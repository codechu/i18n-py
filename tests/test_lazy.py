"""LazyString and lazy_gettext."""

from __future__ import annotations

import gettext as _gettext
from pathlib import Path

from codechu_i18n import LazyString, Translator, lazy_gettext

from _mofile import write_mo


def test_lazy_defers_resolution() -> None:
    calls: list[int] = []

    def resolver() -> str:
        calls.append(1)
        return "resolved"

    s = LazyString(resolver)
    # Not yet called at construction time.
    assert calls == []
    assert str(s) == "resolved"
    assert len(calls) == 1
    # Re-rendered each time (so live locale switches take effect).
    str(s)
    assert len(calls) == 2


def test_lazy_string_equality_and_concat() -> None:
    s = LazyString(lambda: "Hi")
    assert s == "Hi"
    assert s == LazyString(lambda: "Hi")
    assert "i" in s
    assert s + "!" == "Hi!"
    assert "say " + s == "say Hi"


def test_lazy_string_format() -> None:
    s = LazyString(lambda: "Hello {name}!")
    assert s.format(name="Ada") == "Hello Ada!"


def test_lazy_string_mod_formatting() -> None:
    s = LazyString(lambda: "%s items")
    assert s % 3 == "3 items"


def test_lazy_string_repr() -> None:
    s = LazyString(lambda: "hi")
    assert repr(s) == "LazyString('hi')"


def test_lazy_gettext_module_level_resolves_at_render(tmp_path: Path) -> None:
    # Install a translator into the gettext global namespace, then render.
    mo_path = tmp_path / "tr" / "LC_MESSAGES" / "demo.mo"
    write_mo(mo_path, messages={"Pause": "Duraklat"})
    msg = lazy_gettext("Pause")
    # Before install: source returned.
    assert str(msg) == "Pause"
    trans = _gettext.translation("demo", localedir=str(tmp_path), languages=["tr"])
    trans.install()
    try:
        assert str(msg) == "Duraklat"
    finally:
        # Restore builtins so other tests don't see the install.
        import builtins
        del builtins.__dict__["_"]


def test_translator_lazy_gettext(tmp_path: Path) -> None:
    mo_path = tmp_path / "tr" / "LC_MESSAGES" / "demo.mo"
    write_mo(mo_path, messages={"Save": "Kaydet"})
    t = Translator("demo", tmp_path, languages=["tr"])
    msg = t.lazy_gettext("Save")
    assert isinstance(msg, LazyString)
    assert str(msg) == "Kaydet"
