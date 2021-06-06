from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass


# From https://stackoverflow.com/a/32922362/11411477 bc i don't know stuff like this well
import functools


def ignore_args(func, *args, **kwargs):
    @functools.wraps(func)
    def newfunc(*_args, **_kwargs):
        return func(*args, **kwargs)
    return newfunc


__all__ = ["ignore_args"]
