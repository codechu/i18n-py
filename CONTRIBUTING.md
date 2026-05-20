# Contributing to codechu-i18n

Thanks for thinking about contributing. `codechu-i18n` is a stdlib-only
layer over `gettext` — locale negotiation, plural rules, RTL, and a
lazy `Translator`. Patches that stay true to CLDR and RFC 4647 are
warmly received.

## Development setup

```bash
git clone https://github.com/codechu/codechu-i18n-py.git
cd codechu-i18n-py
pip install -e ".[dev]"
pytest -q
ruff check src tests
```

## Workflow

- Branch names: `feature/<short>`, `fix/<short>`, `refactor/<short>`,
  `docs/<short>`, `test/<short>`.
- Commit messages: [Conventional Commits](https://www.conventionalcommits.org/)
  (`feat:`, `fix:`, `refactor:`, `docs:`, `test:`, `chore:`).
- One change per PR — keep diffs reviewable.

## Adding plural rules

When adding a new language family, cite the
[CLDR plural rule chart](https://cldr.unicode.org/index/cldr-spec/plural-rules)
in the commit body and add a parametrized test that exercises at
least one example per category.

## Tests

- `pytest -q` must pass; coverage stays at **≥90 %**.
- New feature → new test. Use the `tests/_mofile.py` helper to write
  `.mo` catalogs from a dict — no `msgfmt` dependency.
- Locale-related code must never touch real `os.environ`. Pass an
  explicit `env` dict.

## Public API discipline

Public surface: `Translator`, `LazyString`, `lazy_gettext`,
`negotiate_locale`, `detect_locale`, `is_rtl`, `plural_form`. Anything
else (`_locale`, `_plural`, `_lazy`, `_translator`) is internal — do
not import from there in downstream code.

## Style

- `ruff check` + `ruff format` clean.
- Type hints on public APIs (`from __future__ import annotations`).
- Use `logging.getLogger(__name__)`; avoid `print`.

## Security

If you find a security issue, see [SECURITY.md](SECURITY.md) — do not
open a public issue for it.

## Developer Certificate of Origin (DCO)

Every commit must be signed off with the [DCO](https://developercertificate.org/).
The sign-off certifies that you wrote the patch, or otherwise have the
right to submit it under the project's license. Add a line to your
commit message:

```
Signed-off-by: Your Name <you@example.com>
```

`git commit -s` does this automatically. PRs without sign-off will
be asked to amend before merge.

Contributions are accepted under the project's license (see
[LICENSE](LICENSE)).
