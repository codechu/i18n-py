# CLAUDE.md — codechu-i18n

Bootstrap per `codechu-org/ai/AGENTS.md` §0 before any work. Prefer
the local clone at `$org_home/codechu-org/ai/AGENTS.md` (if
`~/.config/codechu/config.toml` has `org_home` set); otherwise
WebFetch the public raw URL
<https://raw.githubusercontent.com/codechu/codechu-org/main/ai/AGENTS.md>.
This file lists only product-local overrides.

## Product-local notes

- Stdlib-only. No runtime dependencies. Do not pull in `babel`,
  `ICU`, or anything else without an explicit go-ahead.
- The library never reads ambient state on its own. `detect_locale`
  takes an explicit `env` mapping; callers pass `dict(os.environ)`
  when they want the real environment. Tests pass plain dicts.
- Plural rules follow CLDR. When adding new languages, source the
  rule from <https://cldr.unicode.org/index/cldr-spec/plural-rules>
  and add a parametrized test covering at least one example per
  category.
- `Translator` is lazy: `.mo` loading happens on the first call.
  Keep it that way — tests cover this invariant.
- The carve-out in `STANDARDS.md` §11 applies: this *is* a library
  about i18n, but it must still expose only the mechanism, never
  ship UI strings or `.po` catalogs of its own.

## Discipline reminders (org rules apply)

- Conventional Commits, no AI signature.
- No `--no-verify`, no force push, no unapproved publish.
- See `codechu-org/ai/AGENTS.md` for the full list.
