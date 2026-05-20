# API reference — codechu-i18n

Public surface, version 0.1.0.

## `Translator(domain, locale_dir, languages=None, fallback="en")`

Lazy wrapper around `gettext.translation`. The `.mo` file is opened on
the first call, not at construction.

### Methods

| Method | Description |
|---|---|
| `gettext(msg) -> str` | Translate `msg`; returns source if no catalog matches. |
| `ngettext(singular, plural, n) -> str` | Plural-aware translation using the catalog's `Plural-Forms`. |
| `pgettext(context, msg) -> str` | Context-disambiguated translation. |
| `npgettext(context, singular, plural, n) -> str` | Plural-aware `pgettext`. |
| `format(msg, **kwargs) -> str` | `gettext(msg).format(**kwargs)` — ICU-style placeholders. |
| `lazy_gettext(msg) -> LazyString` | LazyString bound to this translator. |
| `reload() -> None` | Drop the cached catalog and the stdlib `gettext` cache entries for this `locale_dir`. |

## `negotiate_locale(requested, available, *, fallback="en") -> str`

RFC 4647 lookup match. Each `requested` tag is tried against every
`available` tag, progressively shortening it (`zh-Hant-HK` → `zh-Hant`
→ `zh`). First `requested` tag that matches wins. Tag comparison is
case-insensitive and `_`/`-` interchangeable.

## `detect_locale(env=None) -> str`

Resolves a locale tag from a POSIX-style env mapping. Precedence:

1. `LC_ALL`
2. `LC_MESSAGES`
3. `LANG`
4. `LANGUAGE` (colon-separated; first entry wins)

`.codeset` (`.UTF-8`) and `@modifier` (`@euro`) suffixes are stripped.
`C` and `POSIX` values are rejected. Returns `""` when nothing is set.

Caller passes `dict(os.environ)` for the real environment — no implicit
ambient read.

## `is_rtl(locale) -> bool`

`True` for `ar`, `fa`, `he`, `ur`, `ps`, `sd`, `ug`, `yi`, `ckb`, `ks`
(matched on the primary language subtag).

## `plural_form(locale, n) -> int`

CLDR-derived plural category index. Returned integer matches the
`Plural-Forms` index typically used in `.po` headers.

| Family | Languages | Rule |
|---|---|---|
| No plural | `ja ko th vi zh id ms tr az hu fa my km lo` | always `0` |
| English-like | `en de nl es it pt ...` | `1 → 0`, else `1` |
| French-like | `fr`, `pt-BR` | `n ≤ 1 → 0`, else `1` |
| Slavic three-form | `ru uk be sr hr bs` | one / few / many |
| Polish | `pl` | one / few / many |
| Czech / Slovak | `cs sk` | `1`, `2–4`, other |
| Welsh | `cy` | 0 / 1 / 2 / 3 / 6 / other |
| Arabic | `ar` | zero / one / two / few (3–10) / many (11–99) / other |

## `LazyString(resolver)`

String-like proxy that calls `resolver()` on every render. Supports
`str()`, `repr()`, `==`, `in`, `+`, `%`, `.format()`, `len()`.

## `lazy_gettext(msg) -> LazyString`

Module-level lazy string. Resolves via `builtins._` if
`gettext.install()` was called, otherwise via `gettext.gettext`. For a
per-app translator, use `Translator.lazy_gettext` instead.
