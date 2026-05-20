```text
   ┌──────────────────────────────────────────────────┐
   │  c o d e c h u — i 1 8 n                         │
   │   🌐  Hello   Merhaba   مرحبا   你好   שלום       │
   │  ····translate · negotiate · pluralize · RTL···· │
   └──────────────────────────────────────────────────┘
```

[![PyPI](https://img.shields.io/pypi/v/codechu-i18n.svg)](https://pypi.org/project/codechu-i18n/)
[![Python](https://img.shields.io/pypi/pyversions/codechu-i18n.svg)](https://pypi.org/project/codechu-i18n/)
[![CI](https://github.com/codechu/i18n-py/actions/workflows/ci.yml/badge.svg)](https://github.com/codechu/i18n-py/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

> *Internationalization helpers on top of stdlib `gettext`.*

# codechu-i18n

Locale negotiation (RFC 4647), CLDR-derived plural rules, RTL
detection, ICU-style message formatting, and a lazy `Translator`
that defers `.mo` loading until first use. Pure stdlib — this
library does not ship catalogs; that's the consuming app's job.

## Install

```bash
pip install codechu-i18n
```

Python 3.10+. Zero third-party dependencies.

## Quick example

```python
from codechu_i18n import Translator, negotiate_locale, is_rtl, plural_form

# Pick a locale from what the user wants vs what you have.
locale = negotiate_locale(["fr", "tr"], ["tr-TR", "en-US", "de-DE"])
# → "tr-TR"

t = Translator("myapp", "locale", languages=[locale], fallback="en")
t.gettext("Hello")                             # "Merhaba"
t.ngettext("{n} file", "{n} files", 3)         # "3 dosya"
t.format("Hello {name}!", name="Ada")          # "Merhaba Ada!"

is_rtl("ar")            # True   — Arabic, Hebrew, Persian, Urdu, …
plural_form("pl", 5)    # 2 (many) — Polish three-form
plural_form("tr", 5)    # 0       — Turkish has no plural distinction
```

## What you get

- **`Translator`** — lazy `gettext` wrapper with `gettext`,
  `ngettext`, `pgettext`, `npgettext`, and ICU-style
  `format(template, **kwargs)`.
- **`negotiate_locale(requested, available)`** — RFC 4647
  best-match lookup with fallback.
- **`detect_locale(env)`** — `LC_ALL > LC_MESSAGES > LANG > LANGUAGE`
  cascade. The caller supplies the env dict (no implicit
  `os.environ` read).
- **`is_rtl(locale)`** — Arabic, Hebrew, Persian, Urdu, Pashto, and
  the other right-to-left scripts.
- **`plural_form(locale, n)`** — CLDR plural category index;
  handles Slavic three-form, Polish, Arabic six-form, Welsh,
  French zero-as-one, Asian no-plural.
- **`lazy_gettext(msg)`** — module-level strings that resolve at
  render time, so locale switches take effect without re-imports.

This package is a thin layer over `gettext`. It does **not** ship
`.po` / `.mo` catalogs — that's the consuming application's job.
See the
[Codechu library i18n policy](https://github.com/codechu/codechu-org/blob/main/STANDARDS.md)
for the rationale.

## Read more

- [API reference](docs/API.md) — every public symbol with full
  signatures and edge-case tables.
- [Changelog](CHANGELOG.md)

## Family

| Library | Purpose |
|---------|---------|
| [codechu-fmt](https://pypi.org/project/codechu-fmt/) | Human-readable sizes, durations, rates |
| [codechu-cli](https://pypi.org/project/codechu-cli/) | CLI primitives — colors, progress, prompts |
| [codechu-config](https://pypi.org/project/codechu-config/) | Schema-driven config — atomic save, migrations |
| [codechu-log](https://pypi.org/project/codechu-log/) | Structured logging — context, JSON, rotation |
| [codechu-color](https://pypi.org/project/codechu-color/) | Color palettes, WCAG contrast, color-blind variants |

Full ecosystem: [github.com/codechu](https://github.com/codechu).

## Credits

- Plural rules from
  [CLDR](https://cldr.unicode.org/) (Unicode Common Locale Data
  Repository).
- Locale negotiation per
  [RFC 4647](https://www.rfc-editor.org/rfc/rfc4647).
- Built on stdlib `gettext`.

## License

MIT — see [LICENSE](LICENSE).

Part of [Codechu](https://github.com/codechu).
