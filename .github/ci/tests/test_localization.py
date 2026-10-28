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


class ProductLinks(HTMLParser):
    def __init__(self):
        super().__init__()
        self.cards = []
        self.card = None
        self.card_tag = None
        self.in_heading = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        classes = attrs.get("class", "").split()
        if "product-card" in classes or "mini-card" in classes:
            self.card = {"heading": None, "links": []}
            self.card_tag = tag
            self.cards.append(self.card)
        if self.card is None:
            return
        if tag == "h3":
            self.in_heading = True
        if self.in_heading and "data-i18n" in attrs:
            self.card["heading"] = attrs["data-i18n"]
        if tag == "a":
            self.card["links"].append((attrs.get("class"), attrs.get("data-i18n-aria-label")))

    def handle_endtag(self, tag):
        if tag == "h3":
            self.in_heading = False
        if tag == self.card_tag:
            self.card = None
            self.card_tag = None


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

    def test_product_link_names_include_the_target_app_in_both_languages(self):
        parser = ProductLinks()
        parser.feed((ROOT / "index.html").read_text())
        self.assertEqual(len(parser.cards), 19)
        self.assertEqual(sum(len(card["links"]) for card in parser.cards), 32)
        for card in parser.cards:
            self.assertIsNotNone(card["heading"])
            for link_class, label_key in card["links"]:
                self.assertIsNotNone(label_key)
                for language in ("en", "ko"):
                    with self.subTest(app=card["heading"], link=link_class, language=language):
                        app_name = self.messages[card["heading"]][language]
                        self.assertIn(app_name, self.messages[label_key][language])


if __name__ == "__main__":
    unittest.main()
