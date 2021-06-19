from __future__ import annotations

import math
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


def rotate(origin: tuple[float, float], point: tuple[float, float], angle: float) -> tuple[float, float]:
    ox, oy = origin
    px, py = point

    angle = math.radians(angle)

    qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
    qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
    return qx, qy



__all__ = ["ignore_args", "rotate"]
