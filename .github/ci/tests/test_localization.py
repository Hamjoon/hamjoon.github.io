"""Prevent missing translations when homepage content is extended."""

import json
from html.parser import HTMLParser
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[3]


class TranslationMarkers(HTMLParser):
    def __init__(self):
        super().__init__()
        self.keys = set()

    def handle_starttag(self, tag, attrs):
        for name, value in attrs:
            if name in {"data-i18n", "data-i18n-alt", "data-i18n-aria-label"}:
                self.keys.add(value)


class LocalizationTests(unittest.TestCase):
    def setUp(self):
        script = (ROOT / "assets/i18n.js").read_text()
        match = re.search(r"const messages = (\{[\s\S]*?\});\n  const storageKey", script)
        self.assertIsNotNone(match, "The static translation dictionary must be readable")
        self.messages = json.loads(match.group(1))

    def test_all_markers_have_both_languages(self):
        parser = TranslationMarkers()
        parser.feed((ROOT / "index.html").read_text())
        self.assertTrue(parser.keys)
        for key in parser.keys:
            for language in ("en", "ko"):
                with self.subTest(key=key, language=language):
                    self.assertTrue(self.messages.get(key, {}).get(language))

    def test_every_dictionary_entry_has_nonempty_language_values(self):
        for key, entry in self.messages.items():
            with self.subTest(key=key):
                self.assertEqual(set(entry), {"en", "ko"})
                self.assertTrue(all(isinstance(value, str) and value.strip() for value in entry.values()))


if __name__ == "__main__":
    unittest.main()
