"""Translator round-trip: gettext, ngettext, pgettext, format."""

from __future__ import annotations

from pathlib import Path

from codechu_i18n import Translator

from _mofile import write_mo


def _setup_catalog(tmp_path: Path, lang: str, **kwargs: object) -> Path:
    """Write a ``<tmp>/<lang>/LC_MESSAGES/myapp.mo`` and return the locale dir."""
    locale_dir = tmp_path
    mo_path = locale_dir / lang / "LC_MESSAGES" / "myapp.mo"
    write_mo(mo_path, **kwargs)  # type: ignore[arg-type]
    return locale_dir


def test_gettext_basic(tmp_path: Path) -> None:
    locale_dir = _setup_catalog(tmp_path, "tr", messages={"Hello": "Merhaba"})
    t = Translator("myapp", locale_dir, languages=["tr"])
    assert t.gettext("Hello") == "Merhaba"


def test_gettext_missing_returns_source(tmp_path: Path) -> None:
    locale_dir = _setup_catalog(tmp_path, "tr", messages={"Hello": "Merhaba"})
    t = Translator("myapp", locale_dir, languages=["tr"])
    assert t.gettext("Goodbye") == "Goodbye"


def test_gettext_no_catalog_returns_source(tmp_path: Path) -> None:
    # No .mo at all → fallback NullTranslations.
    t = Translator("myapp", tmp_path, languages=["xx"])
    assert t.gettext("Anything") == "Anything"


def test_lazy_loading(tmp_path: Path) -> None:
    t = Translator("myapp", tmp_path / "nope", languages=["tr"])
    # No file access yet.
    assert t._translations is None
    t.gettext("ping")
    assert t._translations is not None


def test_pgettext(tmp_path: Path) -> None:
    locale_dir = _setup_catalog(
        tmp_path,
        "tr",
        messages={},
        contexts={
            ("menu", "Open"): "Aç",
            ("file", "Open"): "Açık",
        },
    )
    t = Translator("myapp", locale_dir, languages=["tr"])
    assert t.pgettext("menu", "Open") == "Aç"
    assert t.pgettext("file", "Open") == "Açık"
    # Missing context falls back to source.
    assert t.pgettext("other", "Open") == "Open"


def test_format_substitutes_placeholders(tmp_path: Path) -> None:
    locale_dir = _setup_catalog(
        tmp_path, "tr", messages={"Hello {name}!": "Merhaba {name}!"}
    )
    t = Translator("myapp", locale_dir, languages=["tr"])
    assert t.format("Hello {name}!", name="Ada") == "Merhaba Ada!"


def test_format_without_catalog_uses_source(tmp_path: Path) -> None:
    t = Translator("myapp", tmp_path / "nope", languages=["tr"])
    assert t.format("Hello {name}!", name="Ada") == "Hello Ada!"


def test_ngettext_english(tmp_path: Path) -> None:
    locale_dir = _setup_catalog(
        tmp_path,
        "en",
        messages={},
        plural_messages={"{n} file": ("{n} files", "{n} file", "{n} files")},
        plural_forms="nplurals=2; plural=(n != 1);",
    )
    t = Translator("myapp", locale_dir, languages=["en"])
    assert t.ngettext("{n} file", "{n} files", 1).format(n=1) == "1 file"
    assert t.ngettext("{n} file", "{n} files", 0).format(n=0) == "0 files"
    assert t.ngettext("{n} file", "{n} files", 2).format(n=2) == "2 files"


def test_ngettext_turkish_single_form(tmp_path: Path) -> None:
    locale_dir = _setup_catalog(
        tmp_path,
        "tr",
        messages={},
        plural_messages={"{n} file": ("{n} files", "{n} dosya")},
        plural_forms="nplurals=1; plural=0;",
    )
    t = Translator("myapp", locale_dir, languages=["tr"])
    # Turkish has no plural distinction — all n collapse to form 0.
    for n in (0, 1, 2, 5, 11):
        assert t.ngettext("{n} file", "{n} files", n).format(n=n) == f"{n} dosya"


def test_ngettext_polish_three_forms(tmp_path: Path) -> None:
    # CLDR Polish: 1 → one, 2-4 (except 12-14) → few, otherwise → many.
    locale_dir = _setup_catalog(
        tmp_path,
        "pl",
        messages={},
        plural_messages={
            "{n} file": ("{n} files", "{n} plik", "{n} pliki", "{n} plików"),
        },
        plural_forms=(
            "nplurals=3; "
            "plural=(n==1 ? 0 : n%10>=2 && n%10<=4 && (n%100<12 || n%100>14) ? 1 : 2);"
        ),
    )
    t = Translator("myapp", locale_dir, languages=["pl"])
    cases = {1: "1 plik", 2: "2 pliki", 3: "3 pliki", 5: "5 plików", 12: "12 plików"}
    for n, expected in cases.items():
        assert t.ngettext("{n} file", "{n} files", n).format(n=n) == expected


def test_reload_drops_cache(tmp_path: Path) -> None:
    locale_dir = _setup_catalog(tmp_path, "tr", messages={"Hi": "Selam"})
    t = Translator("myapp", locale_dir, languages=["tr"])
    assert t.gettext("Hi") == "Selam"
    # Overwrite the .mo with a different translation.
    write_mo(locale_dir / "tr" / "LC_MESSAGES" / "myapp.mo", messages={"Hi": "Merhaba"})
    assert t.gettext("Hi") == "Selam"  # still cached
    t.reload()
    assert t.gettext("Hi") == "Merhaba"
