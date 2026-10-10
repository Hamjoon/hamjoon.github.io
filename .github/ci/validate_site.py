#!/usr/bin/env python3
"""Dependency-free integrity checks for this static GitHub Pages site."""

from __future__ import annotations

import argparse
import bisect
import fnmatch
import os
import re
import sys
from collections import Counter
from dataclasses import dataclass, field
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


BACKUP_PATH_PATTERNS = ("*.bak*", "*_backup.html")
REFERENCE_ATTRIBUTES = {
    "a": ("href",),
    "area": ("href",),
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
    "use": ("href", "xlink:href"),
}
CSS_URL = re.compile(r"url\(\s*(['\"]?)(.*?)\1\s*\)", re.IGNORECASE)
CSS_IMPORT = re.compile(r"@import\s+(['\"])(.*?)\1", re.IGNORECASE)
CSS_COMMENT = re.compile(r"/\*.*?\*/", re.DOTALL)
PRUNED_DIRECTORIES = {".git", ".venv", "node_modules"}


@dataclass
class Document:
    path: Path
    ids: list[tuple[str, int]] = field(default_factory=list)
    named_anchors: list[str] = field(default_factory=list)
    references: list[tuple[str, str, int]] = field(default_factory=list)
    css: list[tuple[str, int]] = field(default_factory=list)
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
        self._in_head = False
        self._in_title = False
        self._title_seen = False
        self._in_style = False
        self._svg_depth = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self._handle_tag(tag, attrs, self_closing=False)

    def _handle_tag(
        self, tag: str, attrs: list[tuple[str, str | None]], *, self_closing: bool
    ) -> None:
        tag = tag.lower()
        values: dict[str, str | None] = {}
        for name, value in attrs:
            values.setdefault(name.lower(), value)
        line = self.getpos()[0]

        if tag == "head" and not self_closing:
            self._in_head = True
        if tag == "svg" and not self_closing:
            self._svg_depth += 1
        if tag == "html" and (values.get("lang") or "").strip():
            self.document.has_lang = True
        if tag == "meta":
            if (values.get("charset") or "").strip():
                self.document.has_charset = True
            http_equiv = (values.get("http-equiv") or "").strip().lower()
            content = values.get("content") or ""
            if http_equiv == "content-type" and re.search(
                r"(?:^|;)\s*charset\s*=\s*[^;\s]+", content, re.IGNORECASE
            ):
                self.document.has_charset = True
            if (values.get("name") or "").lower() == "viewport":
                self.document.has_viewport = True
            if (values.get("property") or "").lower() in {
                "og:image",
                "og:image:url",
                "og:image:secure_url",
            } and content.strip():
                self.document.references.append(("content", content.strip(), line))
        if tag == "main":
            self.document.has_main = True
        if (
            tag == "title"
            and self._in_head
            and not self._svg_depth
            and not self._title_seen
            and not self_closing
        ):
            self._in_title = True
            self._title_seen = True
        if tag == "style" and not self_closing:
            self._in_style = True

        element_id = values.get("id")
        if element_id:
            self.document.ids.append((element_id, line))
        if tag == "a" and values.get("name"):
            self.document.named_anchors.append(values["name"] or "")
        labelled_by = values.get("aria-labelledby")
        if labelled_by:
            self.document.labelled_by.append((labelled_by, line))

        for attribute in REFERENCE_ATTRIBUTES.get(tag, ()):
            value = values.get(attribute)
            if value:
                self.document.references.append((attribute, value.strip(), line))

        inline_style = values.get("style")
        if inline_style:
            self.document.css.append((inline_style, line))

        srcset = values.get("srcset")
        if srcset:
            for url in _srcset_urls(srcset):
                self.document.references.append(("srcset", url, line))

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self._handle_tag(tag, attrs, self_closing=True)

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag == "title":
            self._in_title = False
        elif tag == "head":
            self._in_head = False
            self._in_title = False
        elif tag == "style":
            self._in_style = False
        elif tag == "svg" and self._svg_depth:
            self._svg_depth -= 1

    def handle_data(self, data: str) -> None:
        if self._in_title:
            self.document.title_parts.append(data)
        if self._in_style:
            self.document.css.append((data, self.getpos()[0]))


def _srcset_urls(srcset: str) -> list[str]:
    """Extract srcset URLs without treating commas inside data URLs as separators."""
    urls: list[str] = []
    position = 0
    while position < len(srcset):
        while position < len(srcset) and (srcset[position].isspace() or srcset[position] == ","):
            position += 1
        start = position
        while position < len(srcset) and not srcset[position].isspace():
            position += 1
        url = srcset[start:position]
        stripped = url.rstrip(",")
        if stripped:
            urls.append(stripped)
        if len(stripped) != len(url):
            continue
        while position < len(srcset) and srcset[position] != ",":
            position += 1
        if position < len(srcset):
            position += 1
    return urls


def _is_backup(path: Path, root: Path) -> bool:
    return any(
        fnmatch.fnmatch(part, pattern)
        for part in path.relative_to(root).parts
        for pattern in BACKUP_PATH_PATTERNS
    )


def _site_files(root: Path) -> tuple[list[Path], list[Path]]:
    html_paths: list[Path] = []
    css_paths: list[Path] = []
    for directory, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(
            name
            for name in dirnames
            if name not in PRUNED_DIRECTORIES and not name.startswith(".")
        )
        base = Path(directory)
        for filename in sorted(filenames):
            path = base / filename
            if _is_backup(path, root):
                continue
            if path.suffix.lower() in {".html", ".htm"}:
                html_paths.append(path)
            elif path.suffix.lower() == ".css":
                css_paths.append(path)
    return sorted(html_paths), sorted(css_paths)


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
    target = target.resolve()
    if target.is_dir() or url_path.endswith("/"):
        target /= "index.html"
    elif not target.is_file() and not target.suffix:
        target = target.with_suffix(".html")
    return target, unquote(parsed.fragment)


def _parse_documents(
    root: Path, html_paths: list[Path], errors: list[str]
) -> dict[Path, Document]:
    documents: dict[Path, Document] = {}
    for path in html_paths:
        parser = SiteHTMLParser(path)
        try:
            parser.feed(path.read_text(encoding="utf-8"))
            parser.close()
        except (OSError, UnicodeError) as exc:
            errors.append(f"{_display(path, root)}: cannot parse as UTF-8: {exc}")
            continue
        documents[path.resolve()] = parser.document
    return documents


def _is_published_target(root: Path, target: Path) -> bool:
    try:
        parts = target.relative_to(root).parts
    except ValueError:
        return False
    return not any(part.startswith((".", "_")) for part in parts)


def _check_target(
    root: Path,
    source: Path,
    raw_url: str,
    reference: str,
    fragment_sets: dict[Path, set[str]],
) -> str | None:
    resolved = _resolve_local(root, source, raw_url)
    if resolved is None:
        return None
    target, fragment = resolved
    try:
        target.relative_to(root)
    except ValueError:
        return f"{reference} escapes site root: {raw_url!r}"
    if not _is_published_target(root, target) or not target.is_file():
        return f"missing local target for {reference}: {raw_url!r}"

    if fragment and target.suffix.lower() in {".html", ".htm"}:
        anchor, separator, _directive = fragment.partition(":~:")
        if separator and not anchor:
            return None
        if anchor.lower() == "top":
            return None
        target_fragments = fragment_sets.get(target)
        if target_fragments is None:
            return f"fragment target is not validated: {raw_url!r}"
        if anchor not in target_fragments:
            return f"broken fragment anchor: {raw_url!r}"
    return None


def _strip_css_comments(css: str) -> str:
    return CSS_COMMENT.sub(
        lambda match: "".join("\n" if character == "\n" else " " for character in match.group()),
        css,
    )


def _css_references(css: str, first_line: int = 1) -> list[tuple[str, int]]:
    css = _strip_css_comments(css)
    newline_offsets = [index for index, character in enumerate(css) if character == "\n"]
    matches = [(match.start(), match.group(2)) for match in CSS_URL.finditer(css)]
    matches.extend((match.start(), match.group(2)) for match in CSS_IMPORT.finditer(css))
    return [
        (raw_url.strip(), first_line + bisect.bisect_left(newline_offsets, offset))
        for offset, raw_url in sorted(matches)
        if raw_url.strip()
    ]


def validate_site(root: Path) -> list[str]:
    """Return stable, human-readable validation errors for *root*."""
    root = root.resolve()
    errors: list[str] = []

    required = ("index.html", "404.html", "style.css", "CNAME")
    for relative in required:
        path = root / relative
        if not path.is_file() or path.stat().st_size == 0:
            errors.append(f"{relative}: required site file is missing or empty")

    html_paths, css_paths = _site_files(root)
    documents = _parse_documents(root, html_paths, errors)
    id_sets: dict[Path, set[str]] = {}
    fragment_sets: dict[Path, set[str]] = {}
    for path, document in documents.items():
        relative = _display(path, root)
        counts = Counter(value for value, _line in document.ids)
        id_sets[path] = set(counts)
        fragment_sets[path] = id_sets[path] | set(document.named_anchors)
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
            error = _check_target(root, path, raw_url, attribute, fragment_sets)
            if error:
                errors.append(f"{relative}:{line}: {error}")
        for css, first_line in document.css:
            for raw_url, line in _css_references(css, first_line):
                error = _check_target(root, path, raw_url, "CSS url", fragment_sets)
                if error:
                    errors.append(f"{relative}:{line}: {error}")

    for css_path in css_paths:
        try:
            css = css_path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            errors.append(f"{_display(css_path, root)}: cannot parse as UTF-8: {exc}")
            continue
        for raw_url, line in _css_references(css):
            error = _check_target(root, css_path, raw_url, "CSS url", fragment_sets)
            if error:
                errors.append(f"{_display(css_path, root)}:{line}: {error}")

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
