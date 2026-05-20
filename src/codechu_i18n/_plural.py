"""CLDR-derived plural rules.

Returns a small integer category (0 = "other", and language-specific
indices for "one", "few", "many", etc.) matching the order documented at
https://cldr.unicode.org/index/cldr-spec/plural-rules.

The category numbers match the ``Plural-Forms`` indices commonly used in
``.po`` files so downstream callers can plug them into ``ngettext`` style
catalogs.
"""

from __future__ import annotations

# Languages with no plural distinction (Plural-Forms: nplurals=1).
_NO_PLURAL: frozenset[str] = frozenset(
    {"ja", "ko", "th", "vi", "zh", "id", "ms", "tr", "az", "hu", "fa", "my", "km", "lo"}
)


def _language(locale: str) -> str:
    if not locale:
        return ""
    return locale.replace("_", "-").split("-", 1)[0].lower()


def plural_form(locale: str, n: int) -> int:
    """Return the CLDR plural category index for ``n`` in ``locale``.

    Categories per language family:

    * **No plural** (Asian, Turkic, Persian, Hungarian): always ``0``.
    * **English-like Germanic / Romance** (``en``, ``de``, ``nl``, ``es``,
      ``it``, ``pt``, …): ``0`` for ``n == 1``, ``1`` otherwise.
    * **French / Brazilian Portuguese** (``fr``, ``pt-BR``): ``0`` for
      ``n <= 1`` (treats 0 as singular), ``1`` otherwise. Use the BCP-47
      ``pt-BR`` form to opt in.
    * **Slavic three-form** (``ru``, ``uk``, ``be``, ``sr``, ``hr``,
      ``bs``): ``0`` = one (n%10==1 && n%100!=11); ``1`` = few
      (n%10∈2..4 && n%100∉12..14); ``2`` = many.
    * **Polish** (``pl``): same shape as Slavic three-form but with the
      conventional Polish thresholds.
    * **Czech / Slovak** (``cs``, ``sk``): ``0`` for 1, ``1`` for 2-4,
      ``2`` otherwise.
    * **Welsh** (``cy``): six forms — 0, 1, 2, 3, 6, other.
    * **Arabic** (``ar``): six forms — 0, 1, 2, few (3-10), many (11-99),
      other.
    """
    lang = _language(locale)
    # Region-sensitive: pt-BR uses French-style rule.
    norm = locale.replace("_", "-").lower() if locale else ""
    if norm.startswith("pt-br"):
        return 0 if n <= 1 else 1
    if lang in _NO_PLURAL:
        return 0
    if lang == "fr":
        return 0 if n <= 1 else 1
    if lang == "ar":
        if n == 0:
            return 0
        if n == 1:
            return 1
        if n == 2:
            return 2
        mod100 = n % 100
        if 3 <= mod100 <= 10:
            return 3
        if 11 <= mod100 <= 99:
            return 4
        return 5
    if lang == "cy":
        if n == 0:
            return 0
        if n == 1:
            return 1
        if n == 2:
            return 2
        if n == 3:
            return 3
        if n == 6:
            return 4
        return 5
    if lang in ("cs", "sk"):
        if n == 1:
            return 0
        if 2 <= n <= 4:
            return 1
        return 2
    if lang == "pl":
        if n == 1:
            return 0
        mod10 = n % 10
        mod100 = n % 100
        if 2 <= mod10 <= 4 and not (12 <= mod100 <= 14):
            return 1
        return 2
    if lang in ("ru", "uk", "be", "sr", "hr", "bs"):
        mod10 = n % 10
        mod100 = n % 100
        if mod10 == 1 and mod100 != 11:
            return 0
        if 2 <= mod10 <= 4 and not (12 <= mod100 <= 14):
            return 1
        return 2
    # English-like default: 1 → 0, anything else → 1.
    return 0 if n == 1 else 1
