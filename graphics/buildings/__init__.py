from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass


from graphics.buildings.drill import Drill
from graphics.buildings.mine import Mine
from graphics.buildings.resourceMiner import ResourceMiner
from graphics.buildings.rocket import Rocket

str_to_building = {
    "drill": Drill,
    "mine": Mine,
    "rocket": Rocket
}

building_to_str = dict(zip(str_to_building.values(), str_to_building.keys()))


__all__ = ["str_to_building", building_to_str]
