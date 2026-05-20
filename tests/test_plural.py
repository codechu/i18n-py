"""CLDR plural-form rule tests."""

from __future__ import annotations

import pytest

from codechu_i18n import plural_form


class TestEnglish:
    @pytest.mark.parametrize("n,expected", [(0, 1), (1, 0), (2, 1), (5, 1)])
    def test_basic(self, n: int, expected: int) -> None:
        assert plural_form("en", n) == expected


class TestTurkish:
    @pytest.mark.parametrize("n", [0, 1, 2, 5, 11, 100])
    def test_always_one_form(self, n: int) -> None:
        assert plural_form("tr", n) == 0

    def test_underscored_tag(self) -> None:
        assert plural_form("tr_TR", 42) == 0


class TestPolish:
    @pytest.mark.parametrize(
        "n,expected",
        [(1, 0), (2, 1), (3, 1), (4, 1), (5, 2), (12, 2), (13, 2), (14, 2), (22, 1), (25, 2)],
    )
    def test_three_forms(self, n: int, expected: int) -> None:
        assert plural_form("pl", n) == expected


class TestRussian:
    @pytest.mark.parametrize(
        "n,expected",
        [(1, 0), (21, 0), (2, 1), (4, 1), (5, 2), (11, 2), (12, 2), (22, 1), (25, 2)],
    )
    def test_slavic_three_forms(self, n: int, expected: int) -> None:
        assert plural_form("ru", n) == expected


class TestFrench:
    @pytest.mark.parametrize("n,expected", [(0, 0), (1, 0), (2, 1), (5, 1)])
    def test_zero_is_singular(self, n: int, expected: int) -> None:
        assert plural_form("fr", n) == expected


class TestPortugueseBrazilian:
    def test_pt_br_uses_french_rule(self) -> None:
        assert plural_form("pt-BR", 0) == 0
        assert plural_form("pt-BR", 1) == 0
        assert plural_form("pt-BR", 2) == 1

    def test_pt_pt_uses_english_rule(self) -> None:
        # European Portuguese (no -BR) treats 0 as plural.
        assert plural_form("pt", 0) == 1
        assert plural_form("pt", 1) == 0


class TestArabic:
    @pytest.mark.parametrize(
        "n,expected",
        [(0, 0), (1, 1), (2, 2), (3, 3), (10, 3), (11, 4), (50, 4), (100, 5), (103, 3)],
    )
    def test_six_forms(self, n: int, expected: int) -> None:
        assert plural_form("ar", n) == expected


class TestWelsh:
    @pytest.mark.parametrize(
        "n,expected", [(0, 0), (1, 1), (2, 2), (3, 3), (6, 4), (4, 5), (10, 5)]
    )
    def test_six_forms(self, n: int, expected: int) -> None:
        assert plural_form("cy", n) == expected


class TestCzech:
    @pytest.mark.parametrize("n,expected", [(1, 0), (2, 1), (4, 1), (5, 2), (10, 2)])
    def test_three_forms(self, n: int, expected: int) -> None:
        assert plural_form("cs", n) == expected


class TestEmptyLocale:
    def test_defaults_to_english_rule(self) -> None:
        assert plural_form("", 1) == 0
        assert plural_form("", 2) == 1
