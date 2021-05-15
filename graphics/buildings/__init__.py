from graphics.buildings.drill import Drill
from graphics.buildings.rocket import Rocket

str_to_building = {
    "drill": Drill,
    "rocket": Rocket
}

building_to_str = dict(zip(str_to_building.values(), str_to_building.keys()))
