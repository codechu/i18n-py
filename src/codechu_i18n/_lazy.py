"""Lazy translation strings.

A :class:`LazyString` defers ``gettext`` resolution until the value is
coerced to ``str`` (or compared, concatenated, formatted). Useful for
module-level constants whose translation must reflect the current
locale at *use* time, not import time.
"""

from __future__ import annotations

import builtins
import gettext as _gettext
from collections.abc import Callable


class LazyString:
    """A string-like proxy that calls a resolver on every conversion.

    The resolver is invoked each time the object is rendered, so changing
    the active locale (or installing a new global translator) takes
    effect immediately on the next render.

    ``LazyString`` supports the operations needed for typical UI use:
    ``str()``, ``repr()``, ``==``, ``in``, ``+``, ``%``, ``.format()``,
    and ``len()``. It is not a ``str`` subclass — pass ``str(x)`` if the
    consumer needs an actual ``str``.
    """

    __slots__ = ("_resolver",)

    def __init__(self, resolver: Callable[[], str]) -> None:
        self._resolver = resolver

    def __str__(self) -> str:
        return self._resolver()

    def __repr__(self) -> str:
        return f"LazyString({self._resolver()!r})"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, LazyString):
            return str(self) == str(other)
        if isinstance(other, str):
            return str(self) == other
        return NotImplemented

    def __hash__(self) -> int:
        return hash(str(self))

    def __len__(self) -> int:
        return len(str(self))

    def __contains__(self, item: object) -> bool:
        return item in str(self)

    def __add__(self, other: object) -> str:
        return str(self) + str(other)

    def __radd__(self, other: object) -> str:
        return str(other) + str(self)

    def __mod__(self, args: object) -> str:
        return str(self) % args

    def format(self, *args: object, **kwargs: object) -> str:
        return str(self).format(*args, **kwargs)


def lazy_gettext(msg: str) -> LazyString:
    """Return a :class:`LazyString` that calls ``gettext.gettext(msg)``
    on every render.

    Uses the process-wide default translator installed via
    ``gettext.install()`` (which binds ``_`` in ``builtins``) when
    present, otherwise the stdlib ``gettext.gettext`` fallback. For a
    per-app translator, use :meth:`codechu_i18n.Translator.lazy_gettext`
    instead.
    """

    def resolve() -> str:
        installed = getattr(builtins, "_", None)
        if callable(installed):
            return installed(msg)
        return _gettext.gettext(msg)

    return LazyString(resolve)
