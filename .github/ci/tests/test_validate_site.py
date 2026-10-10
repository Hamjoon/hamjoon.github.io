from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from validate_site import validate_site  # noqa: E402


VALID_INDEX = """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width"><title>Fixture</title>
<link rel="stylesheet" href="/style.css"></head>
<body><main id="main"><h1 id="heading">Fixture</h1>
<section aria-labelledby="heading"><a href="#heading">Heading</a>
<img src="/assets/image.svg" alt=""></section></main></body></html>
"""


class ValidatorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary_directory.name)
        (self.root / "assets").mkdir()
        (self.root / "index.html").write_text(VALID_INDEX, encoding="utf-8")
        (self.root / "404.html").write_text("not found", encoding="utf-8")
        (self.root / "style.css").write_text("body { color: black; }", encoding="utf-8")
        (self.root / "CNAME").write_text("example.com\n", encoding="utf-8")
        (self.root / "assets" / "image.svg").write_text("<svg/>", encoding="utf-8")

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def assert_error_contains(self, text: str) -> None:
        self.assertTrue(
            any(text in error for error in validate_site(self.root)),
            f"expected an error containing {text!r}",
        )

    def replace_index(self, old: str, new: str) -> None:
        path = self.root / "index.html"
        path.write_text(path.read_text(encoding="utf-8").replace(old, new), encoding="utf-8")

    def add_to_main(self, markup: str) -> None:
        self.replace_index("</main>", f"{markup}</main>")

    def test_valid_site_passes(self) -> None:
        self.assertEqual(validate_site(self.root), [])

    def test_missing_local_asset_fails(self) -> None:
        (self.root / "assets" / "image.svg").unlink()
        self.assert_error_contains("missing local target")

    def test_broken_fragment_fails(self) -> None:
        index = (self.root / "index.html").read_text(encoding="utf-8")
        (self.root / "index.html").write_text(
            index.replace('href="#heading"', 'href="#missing"'), encoding="utf-8"
        )
        self.assert_error_contains("broken fragment anchor")

    def test_duplicate_id_fails(self) -> None:
        index = (self.root / "index.html").read_text(encoding="utf-8")
        (self.root / "index.html").write_text(
            index.replace("</main>", '<p id="heading">Again</p></main>'), encoding="utf-8"
        )
        self.assert_error_contains("duplicate id 'heading'")

    def test_missing_aria_labelledby_target_fails(self) -> None:
        index = (self.root / "index.html").read_text(encoding="utf-8")
        (self.root / "index.html").write_text(
            index.replace('aria-labelledby="heading"', 'aria-labelledby="missing"'),
            encoding="utf-8",
        )
        self.assert_error_contains("aria-labelledby target #missing")

    def test_named_anchor_does_not_satisfy_aria_labelledby(self) -> None:
        self.add_to_main('<a name="legacy"></a><section aria-labelledby="legacy"></section>')
        self.assert_error_contains("aria-labelledby target #legacy")

    def test_homepage_regression_fails(self) -> None:
        index = (self.root / "index.html").read_text(encoding="utf-8")
        (self.root / "index.html").write_text(
            index.replace('<meta name="viewport" content="width=device-width">', ""),
            encoding="utf-8",
        )
        self.assert_error_contains("viewport meta tag is required")

    def test_missing_css_asset_fails(self) -> None:
        (self.root / "style.css").write_text(
            "body { background: url('/assets/missing.png'); }", encoding="utf-8"
        )
        self.assert_error_contains("missing local target for CSS url")

    def test_empty_srcset_candidates_do_not_crash(self) -> None:
        self.add_to_main('<img srcset="/assets/image.svg 1x,, " alt="">')
        self.assertEqual(validate_site(self.root), [])

    def test_data_uri_srcset_is_not_split_at_its_comma(self) -> None:
        self.add_to_main('<img srcset="data:image/gif;base64,R0lGOD 1x" alt="">')
        self.assertEqual(validate_site(self.root), [])

    def test_pages_directory_and_extensionless_routes_pass(self) -> None:
        (self.root / "gui.html").write_text("<main>GUI</main>", encoding="utf-8")
        directory = self.root / "cube-serpent"
        directory.mkdir()
        (directory / "index.html").write_text("<main>Cube</main>", encoding="utf-8")
        self.add_to_main('<a href="/gui">GUI</a><a href="/cube-serpent">Cube</a><a href=".">Home</a>')
        self.assertEqual(validate_site(self.root), [])

    def test_svg_title_does_not_satisfy_head_title(self) -> None:
        self.replace_index(
            "<title>Fixture</title>",
            "",
        )
        self.add_to_main("<svg><title>Icon title</title></svg>")
        self.assert_error_contains("non-empty <title> is required")

    def test_self_closing_title_does_not_capture_later_text(self) -> None:
        self.replace_index("<title>Fixture</title>", "<title/>")
        self.assert_error_contains("non-empty <title> is required")

    def test_browser_supported_fragments_pass(self) -> None:
        self.add_to_main(
            '<a name="legacy"></a><a href="#legacy">Legacy</a>'
            '<a href="#top">Top</a><a href="#:~:text=Fixture">Text</a>'
            '<a href="#heading:~:text=Fixture">Heading text</a>'
        )
        self.assertEqual(validate_site(self.root), [])

    def test_http_equiv_charset_passes(self) -> None:
        self.replace_index(
            '<meta charset="utf-8">',
            '<meta http-equiv="Content-Type" content="text/html; charset=utf-8">',
        )
        self.assertEqual(validate_site(self.root), [])

    def test_empty_charset_attribute_fails(self) -> None:
        self.replace_index('<meta charset="utf-8">', "<meta charset>")
        self.assert_error_contains("charset declaration is required")

    def test_first_duplicate_attribute_wins(self) -> None:
        self.add_to_main(
            '<img src="/assets/missing.png" src="/assets/image.svg" alt="">'
        )
        self.assert_error_contains("missing local target for src")

    def test_inline_style_element_and_attribute_are_checked(self) -> None:
        self.add_to_main(
            '<style>.one { background: url("/assets/style-missing.png") }</style>'
            '<div style="background: url(/assets/attribute-missing.png)"></div>'
        )
        errors = validate_site(self.root)
        self.assertTrue(any("style-missing.png" in error for error in errors))
        self.assertTrue(any("attribute-missing.png" in error for error in errors))

    def test_css_import_and_additional_html_reference_forms_are_checked(self) -> None:
        (self.root / "style.css").write_text('@import "missing.css";', encoding="utf-8")
        self.add_to_main(
            '<area href="/missing-map.html">'
            '<svg><use href="/assets/missing-symbol.svg#icon"></use></svg>'
            '<meta property="og:image" content="/assets/missing-og.png">'
        )
        errors = validate_site(self.root)
        for missing in ("missing.css", "missing-map.html", "missing-symbol.svg", "missing-og.png"):
            self.assertTrue(any(missing in error for error in errors), missing)

    def test_svg_use_fragment_is_checked(self) -> None:
        self.add_to_main('<svg><use href="#missing-symbol"></use></svg>')
        self.assert_error_contains("broken fragment anchor")

    def test_css_comment_newlines_preserve_error_line_number(self) -> None:
        (self.root / "style.css").write_text(
            "/*\nlicense\nline\nline\n*/\nbody { background: url(missing.png); }",
            encoding="utf-8",
        )
        self.assert_error_contains("style.css:6: missing local target for CSS url")

    def test_backup_directories_are_excluded_for_html_and_css(self) -> None:
        backup = self.root / "old.bak"
        backup.mkdir()
        (backup / "page.html").write_text('<img src="missing.png">', encoding="utf-8")
        (backup / "style.css").write_text("a{background:url(missing.png)}", encoding="utf-8")
        self.assertEqual(validate_site(self.root), [])

    def test_working_directories_are_pruned(self) -> None:
        for name in (".git", ".venv", "node_modules"):
            directory = self.root / name
            directory.mkdir()
            (directory / "style.css").write_text("a{background:url(missing.png)}", encoding="utf-8")
        self.assertEqual(validate_site(self.root), [])

    def test_jekyll_excluded_local_target_fails(self) -> None:
        private = self.root / "_private"
        private.mkdir()
        (private / "asset.svg").write_text("<svg/>", encoding="utf-8")
        self.add_to_main('<img src="/_private/asset.svg" alt="">')
        self.assert_error_contains("missing local target for src")


if __name__ == "__main__":
    unittest.main()
