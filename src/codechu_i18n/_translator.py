"""The :class:`Translator` — a lazy wrapper around stdlib ``gettext``."""

from __future__ import annotations

import gettext as _gettext
from pathlib import Path
from typing import TYPE_CHECKING

from ._lazy import LazyString

if TYPE_CHECKING:
    from collections.abc import Sequence


class Translator:
    """Lazy ``gettext`` wrapper with ICU-style :meth:`format` and contexts.

    ``domain``
        gettext domain (``.mo`` basename).
    ``locale_dir``
        Directory containing ``<lang>/LC_MESSAGES/<domain>.mo`` files.
    ``languages``
        Ordered preference list (``["tr-TR", "tr", "en"]``). When ``None``
        gettext falls back to ``LANGUAGE``/``LC_ALL``/``LC_MESSAGES``/``LANG``.
    ``fallback``
        Tag used when no ``.mo`` is found. The English-fallback rule of
        ``gettext.translation(..., fallback=True)`` is honored: missing
        catalogs return the source string verbatim instead of raising.

    The underlying catalog is loaded lazily on the first lookup. Repeated
    lookups reuse the same translations instance.
    """

    def __init__(
        self,
        domain: str,
        locale_dir: str | Path,
        languages: Sequence[str] | None = None,
        fallback: str = "en",
    ) -> None:
        self.domain = domain
        self.locale_dir = Path(locale_dir)
        self.languages = list(languages) if languages is not None else None
        self.fallback = fallback
        self._translations: _gettext.NullTranslations | None = None

    @property
    def translations(self) -> _gettext.NullTranslations:
        """Lazily-loaded :class:`gettext.NullTranslations`."""
        if self._translations is None:
            self._translations = _gettext.translation(
                self.domain,
                localedir=str(self.locale_dir),
                languages=self.languages,
                fallback=True,
            )
        return self._translations

    def gettext(self, msg: str) -> str:
        """Translate ``msg``. Returns the source string if no catalog matches."""
        return self.translations.gettext(msg)

    def ngettext(self, singular: str, plural: str, n: int) -> str:
        """Translate ``singular``/``plural`` based on ``n`` using the catalog's
        ``Plural-Forms`` header. Falls back to English-style ``n==1`` if no
        catalog is installed.
        """
        return self.translations.ngettext(singular, plural, n)

    def pgettext(self, context: str, msg: str) -> str:
        """Translate ``msg`` in a disambiguating ``context``.

        Mirrors GNU gettext's ``pgettext`` — the catalog key is
        ``context\\x04msg``; if no translation exists, ``msg`` is returned
        unchanged.
        """
        return self.translations.pgettext(context, msg)

    def npgettext(self, context: str, singular: str, plural: str, n: int) -> str:
        """Plural-aware :meth:`pgettext`."""
        return self.translations.npgettext(context, singular, plural, n)

    def format(self, msg: str, /, **kwargs: object) -> str:
        """Translate ``msg`` then apply ``str.format(**kwargs)``.

        ICU-style placeholders (``"Hello {name}!"``) are resolved against
        ``kwargs``. Missing keys raise ``KeyError`` (same as
        :meth:`str.format`). For a forgiving variant, format the result
        of :meth:`gettext` yourself.
        """
        return self.gettext(msg).format(**kwargs)

    def lazy_gettext(self, msg: str) -> LazyString:
        """Return a :class:`LazyString` bound to this translator."""
        return LazyString(lambda: self.gettext(msg))

    def reload(self) -> None:
        """Drop the cached catalog so the next call reloads from disk.

        Also clears the global ``gettext`` module-level cache for this
        ``(domain, locale_dir, languages)`` tuple — stdlib ``gettext``
        memoizes parsed ``.mo`` files indefinitely, which would otherwise
        keep the old translations alive after :meth:`reload`.
        """
        self._translations = None
        # stdlib gettext keys its cache by (class, mofile_path); drop any
        # entry whose path lives under this translator's locale_dir.
        cache = getattr(_gettext, "_translations", None)
        if isinstance(cache, dict):
            prefix = str(self.locale_dir)
            for key in [k for k in cache if isinstance(k, tuple) and len(k) >= 2 and isinstance(k[1], str) and k[1].startswith(prefix)]:
                cache.pop(key, None)
