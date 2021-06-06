from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass


from graphics.buildings.resourceMiner import ResourceMiner


class Drill(ResourceMiner):
    __type__: str = "drill"

    def __init__(self, *args, **kwargs):
        ResourceMiner.__init__(self, *args, **kwargs)


__all__ = ["Drill"]
