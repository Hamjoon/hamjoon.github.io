# Homepage languages

- First visits use English, even when the browser language is Korean.
- The header offers EN / 한국어 buttons. An explicit choice is saved in
  `localStorage` under `garibong.language` (`en` or `ko`).
- Storage failures do not prevent switching; invalid stored values fall back to
  English. With JavaScript disabled, English remains usable and controls stay hidden.
- `assets/i18n.js` contains the English/Korean dictionary. `data-i18n` markers
  identify text; `data-i18n-alt` and `data-i18n-aria-label` identify accessible text.
  Values are assigned with textContent, never interpreted as HTML.
- The document language, page title, description and Open Graph text follow the
  selection. URLs, native app links, contact details and section anchors stay fixed.
- New content needs both translations and explicit markers. The CI localization
  checks ensure every referenced key has both languages.
- This is a single-page language switch, not separate locale URLs. Shared links
  and no-JavaScript search previews retain the default English content.

Run checks with `python3 -m unittest discover -s .github/ci/tests -v` and
`python3 .github/ci/validate_site.py .`.
