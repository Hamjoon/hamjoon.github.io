#!/usr/bin/env python3
"""Dependency-free integrity checks for this static GitHub Pages site."""

from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from dataclasses import dataclass, field
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


BACKUP_HTML_PATTERNS = ("*.bak*", "*_backup.html")
REFERENCE_ATTRIBUTES = {
    "a": ("href",),
    "audio": ("src",),
    "embed": ("src",),
    "iframe": ("src",),
    "img": ("src",),
    "input": ("src",),
    "link": ("href",),
    "object": ("data",),
    "script": ("src",),
    "source": ("src",),
    "track": ("src",),
    "video": ("poster", "src"),
}
CSS_URL = re.compile(r"url\(\s*(['\"]?)(.*?)\1\s*\)", re.IGNORECASE)
CSS_COMMENT = re.compile(r"/\*.*?\*/", re.DOTALL)


@dataclass
class Document:
    path: Path
    ids: list[tuple[str, int]] = field(default_factory=list)
    references: list[tuple[str, str, int]] = field(default_factory=list)
    labelled_by: list[tuple[str, int]] = field(default_factory=list)
    has_lang: bool = False
    has_charset: bool = False
    has_viewport: bool = False
    has_main: bool = False
    title_parts: list[str] = field(default_factory=list)


class SiteHTMLParser(HTMLParser):
    def __init__(self, path: Path) -> None:
        super().__init__(convert_charrefs=True)
        self.document = Document(path)
        self._in_title = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        values = {name.lower(): value for name, value in attrs}
        line = self.getpos()[0]

        if tag == "html" and (values.get("lang") or "").strip():
            self.document.has_lang = True
        if tag == "meta":
            if "charset" in values:
                self.document.has_charset = True
            if (values.get("name") or "").lower() == "viewport":
                self.document.has_viewport = True
        if tag == "main":
            self.document.has_main = True
        if tag == "title":
            self._in_title = True

        element_id = values.get("id")
        if element_id:
            self.document.ids.append((element_id, line))
        labelled_by = values.get("aria-labelledby")
        if labelled_by:
            self.document.labelled_by.append((labelled_by, line))

        for attribute in REFERENCE_ATTRIBUTES.get(tag, ()):
            value = values.get(attribute)
            if value:
                self.document.references.append((attribute, value.strip(), line))

        srcset = values.get("srcset")
        if srcset:
            for candidate in srcset.split(","):
                url = candidate.strip().split(maxsplit=1)[0]
                if url:
                    self.document.references.append(("srcset", url, line))

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.handle_starttag(tag, attrs)

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "title":
            self._in_title = False

    def handle_data(self, data: str) -> None:
        if self._in_title:
            self.document.title_parts.append(data)


def _production_html(root: Path) -> list[Path]:
    excluded: set[Path] = set()
    for pattern in BACKUP_HTML_PATTERNS:
        excluded.update(root.rglob(pattern))
    return sorted(path for path in root.rglob("*.html") if path not in excluded)


def _display(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return str(path)


def _resolve_local(root: Path, source: Path, raw_url: str) -> tuple[Path, str] | None:
    if not raw_url or raw_url.startswith("//"):
        return None
    parsed = urlsplit(raw_url)
    if parsed.scheme or parsed.netloc:
        return None

    url_path = unquote(parsed.path)
    if not url_path:
        target = source
    elif url_path.startswith("/"):
        target = root / url_path.lstrip("/")
    else:
        target = source.parent / url_path
    if url_path.endswith("/") or (url_path == "/"):
        target = target / "index.html"

    target = target.resolve()
    try:
        target.relative_to(root.resolve())
    except ValueError:
        return target, parsed.fragment
    return target, unquote(parsed.fragment)


def _parse_documents(root: Path, errors: list[str]) -> dict[Path, Document]:
    documents: dict[Path, Document] = {}
    for path in _production_html(root):
        parser = SiteHTMLParser(path)
        try:
            parser.feed(path.read_text(encoding="utf-8"))
            parser.close()
        except (OSError, UnicodeError) as exc:
            errors.append(f"{_display(path, root)}: cannot parse as UTF-8: {exc}")
            continue
        documents[path.resolve()] = parser.document
    return documents


def validate_site(root: Path) -> list[str]:
    """Return stable, human-readable validation errors for *root*."""
    root = root.resolve()
    errors: list[str] = []

    required = ("index.html", "404.html", "style.css", "CNAME")
    for relative in required:
        path = root / relative
        if not path.is_file() or path.stat().st_size == 0:
            errors.append(f"{relative}: required site file is missing or empty")

    documents = _parse_documents(root, errors)
    id_sets: dict[Path, set[str]] = {}
    for path, document in documents.items():
        relative = _display(path, root)
        counts = Counter(value for value, _line in document.ids)
        id_sets[path] = set(counts)
        for value, count in sorted(counts.items()):
            if count > 1:
                lines = [str(line) for item, line in document.ids if item == value]
                errors.append(
                    f"{relative}:{','.join(lines)}: duplicate id {value!r} ({count} occurrences)"
                )
        for value, line in document.labelled_by:
            for target_id in value.split():
                if target_id not in id_sets[path]:
                    errors.append(
                        f"{relative}:{line}: aria-labelledby target #{target_id} does not exist"
                    )

    homepage = documents.get((root / "index.html").resolve())
    if homepage:
        homepage_checks = (
            (homepage.has_lang, "index.html: <html> must have a non-empty lang attribute"),
            (homepage.has_charset, "index.html: a charset declaration is required"),
            (homepage.has_viewport, "index.html: a viewport meta tag is required"),
            (homepage.has_main, "index.html: a <main> landmark is required"),
            (bool("".join(homepage.title_parts).strip()), "index.html: a non-empty <title> is required"),
        )
        errors.extend(message for passed, message in homepage_checks if not passed)

    for path, document in documents.items():
        relative = _display(path, root)
        for attribute, raw_url, line in document.references:
            resolved = _resolve_local(root, path, raw_url)
            if resolved is None:
                continue
            target, fragment = resolved
            try:
                target.relative_to(root)
            except ValueError:
                errors.append(f"{relative}:{line}: {attribute} escapes site root: {raw_url!r}")
                continue
            if not target.is_file():
                errors.append(f"{relative}:{line}: missing local target for {attribute}: {raw_url!r}")
                continue
            if fragment and target.suffix.lower() in (".html", ".htm"):
                target_ids = id_sets.get(target)
                if target_ids is None:
                    errors.append(f"{relative}:{line}: fragment target is not validated: {raw_url!r}")
                elif fragment not in target_ids:
                    errors.append(f"{relative}:{line}: broken fragment anchor: {raw_url!r}")

    for css_path in sorted(root.rglob("*.css")):
        try:
            css = CSS_COMMENT.sub("", css_path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError) as exc:
            errors.append(f"{_display(css_path, root)}: cannot parse as UTF-8: {exc}")
            continue
        for match in CSS_URL.finditer(css):
            raw_url = match.group(2).strip()
            resolved = _resolve_local(root, css_path, raw_url)
            if resolved is None:
                continue
            target, _fragment = resolved
            line = css.count("\n", 0, match.start()) + 1
            try:
                target.relative_to(root)
            except ValueError:
                errors.append(
                    f"{_display(css_path, root)}:{line}: CSS url escapes site root: {raw_url!r}"
                )
                continue
            if not target.is_file():
                errors.append(
                    f"{_display(css_path, root)}:{line}: missing local target for CSS url: {raw_url!r}"
                )

    return sorted(errors)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", type=Path, default=Path.cwd())
    args = parser.parse_args(argv)
    errors = validate_site(args.root)
    if errors:
        print(f"Site validation failed with {len(errors)} error(s):", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print("Site validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
