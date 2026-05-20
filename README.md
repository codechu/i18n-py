```text
   ┌──────────────────────────────────────────────────┐
   │  c o d e c h u — i 1 8 n                         │
   │   🌐  Hello   Merhaba   مرحبا   你好   שלום       │
   │  ····translate · negotiate · pluralize · RTL···· │
   └──────────────────────────────────────────────────┘
```

> *Internationalization helpers on top of stdlib `gettext`.*

# codechu-i18n

Locale negotiation (RFC 4647), CLDR-derived plural rules, RTL
detection, ICU-style message formatting, and a lazy `Translator` that
defers `.mo` loading until first use. Pure stdlib. Python 3.10+.

```bash
pip install codechu-i18n
```

## What it gives you

- **`Translator`** — lazy `gettext` wrapper with `gettext`, `ngettext`,
  `pgettext`, `npgettext`, and ICU-style `format("Hello {name}!", name=…)`.
- **`negotiate_locale(requested, available)`** — RFC 4647 lookup match.
- **`detect_locale(env)`** — `LC_ALL > LC_MESSAGES > LANG > LANGUAGE`,
  caller passes the env dict (no implicit `os.environ`).
- **`is_rtl(locale)`** — Arabic, Hebrew, Persian, Urdu, Pashto, …
- **`plural_form(locale, n)`** — CLDR plural category index (handles
  Slavic three-form, Polish, Arabic six-form, Welsh, French zero-as-one,
  Asian no-plural).
- **`lazy_gettext(msg)`** — module-level strings that resolve at render
  time, not import time.

## Quick examples

### Translator

```python
from codechu_i18n import Translator

t = Translator("myapp", "locale", languages=["tr"], fallback="en")

t.gettext("Hello")                            # "Merhaba"
t.ngettext("{n} file", "{n} files", 3)        # "3 dosya"
t.pgettext("menu", "Open")                    # context-disambiguated
t.format("Hello {name}!", name="Ada")         # "Merhaba Ada!"
```

### Locale negotiation

```python
from codechu_i18n import negotiate_locale

available = ["tr-TR", "en-US", "de-DE"]
negotiate_locale(["fr", "tr"], available)        # "tr-TR"
negotiate_locale(["zh-Hant-HK"], ["zh-Hant"])    # "zh-Hant"
negotiate_locale(["xx"], available, fallback="en")  # "en"
```

### Detect from env

```python
import os
from codechu_i18n import detect_locale

detect_locale(dict(os.environ))   # "tr-TR" on a Turkish machine
detect_locale({})                 # ""  (no implicit ambient read)
```

### RTL and plural rules

```python
from codechu_i18n import is_rtl, plural_form

is_rtl("ar")          # True
is_rtl("tr-TR")       # False

plural_form("en", 1)  # 0 (one)
plural_form("en", 2)  # 1 (other)
plural_form("pl", 3)  # 1 (few)
plural_form("pl", 5)  # 2 (many)
plural_form("ar", 0)  # 0 (zero)
plural_form("tr", 5)  # 0 (Turkish has no plural distinction)
```

### Lazy strings

```python
from codechu_i18n import lazy_gettext as _

# Resolved every time str() is called — locale switches take effect.
GREETING = _("Hello")
print(str(GREETING))   # uses current installed translator
```

## Library policy

This package is a thin layer over `gettext`. It does **not** ship
`.po`/`.mo` catalogs — that is the consuming application's job. See the
[Codechu standards on library i18n](https://github.com/codechu/codechu-org/blob/main/STANDARDS.md)
for the rationale.

## License

MIT — see [LICENSE](LICENSE).

Part of [Codechu](https://github.com/codechu).
