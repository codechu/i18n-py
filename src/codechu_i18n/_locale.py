"""Locale tag handling: negotiation (RFC 4647 lookup), detection, RTL."""

from __future__ import annotations

from collections.abc import Iterable, Mapping

# Languages written right-to-left. ISO 639-1 codes; ``ckb`` (Central Kurdish)
# and ``ks`` (Kashmiri) and ``ps`` (Pashto) and ``sd`` (Sindhi) and ``yi``
# (Yiddish) included for completeness.
_RTL_LANGS: frozenset[str] = frozenset(
    {"ar", "fa", "he", "ur", "ps", "sd", "ug", "yi", "ckb", "ks"}
)


def _normalize(tag: str) -> str:
    """Normalize a BCP-47 tag to ``ll`` or ``ll-RR`` form.

    Splits on ``-`` or ``_``; language is lowercased, region is uppercased,
    script (4 chars) is title-cased. Empty input returns empty string.
    """
    if not tag:
        return ""
    parts = tag.replace("_", "-").split("-")
    out = [parts[0].lower()]
    for p in parts[1:]:
        if len(p) == 4:
            out.append(p.title())
        elif len(p) in (2, 3) and p.isalpha():
            out.append(p.upper())
        else:
            out.append(p)
    return "-".join(out)


def _language(tag: str) -> str:
    """Return the primary language subtag, lowercased."""
    if not tag:
        return ""
    return tag.replace("_", "-").split("-", 1)[0].lower()


def negotiate_locale(
    requested: Iterable[str],
    available: Iterable[str],
    *,
    fallback: str = "en",
) -> str:
    """Pick the best ``available`` tag for the ``requested`` preferences.

    Implements an RFC 4647 *lookup* match: each requested tag is tried
    against every available tag, progressively shortening it (``zh-Hant-HK``
    → ``zh-Hant`` → ``zh``) until a match is found. The first ``requested``
    tag that produces a match wins.

    Both lists are normalized (case-insensitive, ``_``/``-`` interchangeable).
    Returns ``fallback`` when nothing matches.
    """
    avail = [(_normalize(a), a) for a in available if a]
    if not avail:
        return fallback
    norm_avail = {n: orig for n, orig in avail}
    # Also index by language-only for the final broaden step.
    by_lang: dict[str, str] = {}
    for n, orig in avail:
        lang = n.split("-", 1)[0]
        by_lang.setdefault(lang, orig)

    for r in requested:
        if not r:
            continue
        nr = _normalize(r)
        # Exact normalized match.
        if nr in norm_avail:
            return norm_avail[nr]
        # Progressive truncation: drop trailing subtags one at a time.
        parts = nr.split("-")
        while len(parts) > 1:
            parts.pop()
            candidate = "-".join(parts)
            if candidate in norm_avail:
                return norm_avail[candidate]
        # Final broaden: any available tag sharing the requested language.
        lang = nr.split("-", 1)[0]
        if lang in by_lang:
            return by_lang[lang]
    return fallback


def detect_locale(env: Mapping[str, str] | None = None) -> str:
    """Detect a locale tag from a POSIX-style ``env`` mapping.

    Honors ``LC_ALL`` > ``LC_MESSAGES`` > ``LANG`` > ``LANGUAGE`` (the latter
    is colon-separated; the first entry wins). Strips the codeset
    (``.UTF-8``) and modifier (``@euro``) suffixes. Returns the normalized
    tag or an empty string if nothing is set.

    Callers pass ``dict(os.environ)`` for the real environment; ``None``
    is treated as an empty mapping (no implicit ambient read).
    """
    if env is None:
        env = {}
    for var in ("LC_ALL", "LC_MESSAGES", "LANG"):
        value = env.get(var)
        if value and value not in ("C", "POSIX"):
            return _strip(value)
    language = env.get("LANGUAGE")
    if language:
        first = language.split(":", 1)[0]
        if first and first not in ("C", "POSIX"):
            return _strip(first)
    return ""


def _strip(value: str) -> str:
    """Remove ``.codeset`` and ``@modifier`` suffixes, then normalize."""
    value = value.split("@", 1)[0]
    value = value.split(".", 1)[0]
    return _normalize(value)


def is_rtl(locale: str) -> bool:
    """Return ``True`` if ``locale``'s primary language is written RTL.

    Currently: Arabic (``ar``), Hebrew (``he``), Persian (``fa``), Urdu
    (``ur``), Pashto (``ps``), Sindhi (``sd``), Uyghur (``ug``), Yiddish
    (``yi``), Central Kurdish (``ckb``), Kashmiri (``ks``).
    """
    return _language(locale) in _RTL_LANGS
