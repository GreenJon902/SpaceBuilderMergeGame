from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass


from graphics.buildings.buildingbase import BuildingBase


class Rocket(BuildingBase):
    __type__: str = "rocket"

    movable: bool = False

    def __init__(self, *args, **kwargs):
        BuildingBase.__init__(self, *args, **kwargs)

    def get_buttons(self) -> list[str]:
        buttons = BuildingBase.get_buttons(self)
        buttons.append("scrap")

        buttons.remove("store")

        return buttons


__all__ = ["Rocket"]
