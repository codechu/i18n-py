"""Internationalization helpers on top of stdlib ``gettext``.

Locale negotiation (RFC 4647), CLDR-derived plural rules, RTL detection,
ICU-style message formatting, and a lazy :class:`Translator` that defers
``.mo`` loading until the first lookup. Pure stdlib, Python 3.10+.

The library never reads ambient state on its own — callers that want the
process environment pass an explicit ``env`` mapping to
:func:`detect_locale`. This keeps tests hermetic.

Quick start::

    from codechu_i18n import Translator

    t = Translator("myapp", "locale", languages=["tr"], fallback="en")
    t.gettext("Hello")                            # "Merhaba"
    t.ngettext("{n} file", "{n} files", 3)        # "3 files"
    t.format("Hello {name}!", name="Ada")         # "Hello Ada!"
"""

from __future__ import annotations

from ._lazy import LazyString, lazy_gettext
from ._locale import detect_locale, is_rtl, negotiate_locale
from ._plural import plural_form
from ._translator import Translator

__version__ = "0.1.0"
__all__ = [
    "LazyString",
    "Translator",
    "detect_locale",
    "is_rtl",
    "lazy_gettext",
    "negotiate_locale",
    "plural_form",
]
