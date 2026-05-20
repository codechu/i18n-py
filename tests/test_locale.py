"""Locale negotiation, detection, and RTL."""

from __future__ import annotations

import pytest

from codechu_i18n import detect_locale, is_rtl, negotiate_locale


class TestNegotiate:
    def test_exact_match(self) -> None:
        assert negotiate_locale(["tr-TR"], ["tr-TR", "en-US"]) == "tr-TR"

    def test_case_insensitive(self) -> None:
        assert negotiate_locale(["TR-tr"], ["tr-TR"]) == "tr-TR"

    def test_underscore_form(self) -> None:
        assert negotiate_locale(["tr_TR"], ["tr-TR"]) == "tr-TR"

    def test_first_requested_wins(self) -> None:
        # fr not available, tr available → tr.
        assert negotiate_locale(["fr", "tr"], ["tr-TR", "en-US"]) == "tr-TR"

    def test_truncation(self) -> None:
        # request zh-Hant-HK, only zh-Hant available → broaden.
        assert negotiate_locale(["zh-Hant-HK"], ["zh-Hant", "zh-Hans"]) == "zh-Hant"

    def test_broaden_to_language(self) -> None:
        # request de-CH, only de-DE available → match by language.
        assert negotiate_locale(["de-CH"], ["de-DE", "en-US"]) == "de-DE"

    def test_fallback_when_nothing_matches(self) -> None:
        assert negotiate_locale(["xx"], ["en", "tr"], fallback="en") == "en"

    def test_fallback_empty_available(self) -> None:
        assert negotiate_locale(["tr"], [], fallback="en") == "en"

    def test_skip_empty_strings(self) -> None:
        assert negotiate_locale(["", "tr"], ["", "tr-TR"]) == "tr-TR"


class TestDetectLocale:
    def test_lc_all_wins(self) -> None:
        env = {"LC_ALL": "tr_TR.UTF-8", "LC_MESSAGES": "en_US.UTF-8", "LANG": "fr_FR"}
        assert detect_locale(env) == "tr-TR"

    def test_lc_messages_before_lang(self) -> None:
        assert detect_locale({"LC_MESSAGES": "en_US.UTF-8", "LANG": "fr_FR"}) == "en-US"

    def test_lang_fallback(self) -> None:
        assert detect_locale({"LANG": "tr_TR.UTF-8"}) == "tr-TR"

    def test_language_var_first_colon_entry(self) -> None:
        assert detect_locale({"LANGUAGE": "tr:en:de"}) == "tr"

    def test_strips_modifier(self) -> None:
        assert detect_locale({"LANG": "de_DE.UTF-8@euro"}) == "de-DE"

    def test_empty_env(self) -> None:
        assert detect_locale({}) == ""

    def test_none_env_treated_as_empty(self) -> None:
        assert detect_locale(None) == ""

    def test_c_locale_ignored(self) -> None:
        assert detect_locale({"LANG": "C"}) == ""

    def test_posix_locale_ignored(self) -> None:
        assert detect_locale({"LC_ALL": "POSIX", "LANG": "tr_TR"}) == "tr-TR"


class TestIsRTL:
    @pytest.mark.parametrize("locale", ["ar", "ar-SA", "he", "he-IL", "fa", "fa_IR", "ur", "ps", "ckb"])
    def test_rtl_languages(self, locale: str) -> None:
        assert is_rtl(locale) is True

    @pytest.mark.parametrize("locale", ["en", "en-US", "tr", "tr-TR", "de", "fr", "zh-Hans", ""])
    def test_ltr_languages(self, locale: str) -> None:
        assert is_rtl(locale) is False
