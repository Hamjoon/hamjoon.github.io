from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
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


if __name__ == "__main__":
    unittest.main()
