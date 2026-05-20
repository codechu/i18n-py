# Security policy

`codechu-i18n` parses locale tags from caller-supplied environment
mappings, negotiates against caller-supplied lists, and loads
`gettext` `.mo` catalogs from caller-supplied directories. Anything
that lets a hostile value escape those boundaries — or that lets a
malformed `.mo` crash the host process — is security-relevant.

## Supported versions

| Version | Supported |
|---|:---:|
| `main` branch | ✅ |
| Latest minor release (0.x) | ✅ |
| Older releases | ❌ |

Pre-1.0.0 period — only the latest minor receives security fixes.

## Reporting a vulnerability

### Preferred path — GitHub Security Advisory (private)

Open a **private** advisory at
[github.com/codechu/codechu-i18n-py/security/advisories/new](https://github.com/codechu/codechu-i18n-py/security/advisories/new).

### Alternative — Email

Write to `security@codechu.com`.

## Scope — what to report

**In scope:**

- **Locale tag injection** — characters in a requested tag that
  break `negotiate_locale`'s match logic (e.g. NUL, path
  separators that leak into downstream `.mo` lookups).
- **`detect_locale` failures** on adversarial env values
  (extremely long strings, embedded NULs, malformed `@modifier`
  / `.codeset` suffixes).
- **Plural-form integer overflow** — extreme `n` causing wrong
  category.
- **`LazyString` re-render side effects** — a resolver that
  observes state it shouldn't.

**Out of scope:**

- Bugs in stdlib `gettext` itself (report upstream to CPython).
- Callers passing an attacker-controlled `locale_dir` to
  `Translator` — that is an upstream caller bug, but we still
  happily harden the input check if you propose one.
- Translation correctness disputes (those are bug reports, not
  security issues).

## Process

Reports are reviewed on a best-effort basis — no fixed SLA. We aim
for coordinated disclosure within **90 days** of the report,
extendable by mutual agreement.

Public disclosure is coordinated after the fix is released
(together with the reporter).

## Public disclosure

Once a confirmed fix is released:

- A summary is added to the CHANGELOG under the `### Security`
  category (with the reporter's name if they want credit).
- A GitHub Security Advisory is published.
- If a CVE was assigned, its number is referenced.
