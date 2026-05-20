# Changelog

[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) + [SemVer](https://semver.org/).

## [Unreleased]

## [0.1.0] — 2026-05-20

### Added
- `Translator(domain, locale_dir, languages=None, fallback="en")` — lazy
  wrapper around `gettext.translation` with `gettext`, `ngettext`,
  `pgettext`, `npgettext`, `format(...)`, `lazy_gettext(...)`, and
  `reload()`.
- `negotiate_locale(requested, available, fallback="en")` — RFC 4647
  lookup match with progressive subtag truncation and language-only
  broadening.
- `detect_locale(env)` — POSIX env var resolution
  (`LC_ALL > LC_MESSAGES > LANG > LANGUAGE`); strips `.codeset` /
  `@modifier`; rejects `C` / `POSIX`.
- `is_rtl(locale)` — covers Arabic, Hebrew, Persian, Urdu, Pashto,
  Sindhi, Uyghur, Yiddish, Central Kurdish, Kashmiri.
- `plural_form(locale, n)` — CLDR rules for English-like, French,
  Brazilian Portuguese, Slavic three-form, Polish, Czech/Slovak, Welsh,
  Arabic, and Asian no-plural languages.
- `LazyString` and `lazy_gettext(msg)` — defer translation until render.
