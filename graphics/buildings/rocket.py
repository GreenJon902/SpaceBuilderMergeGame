from graphics.buildings.buildingbase import BuildingBase


class Rocket(BuildingBase):
    movable: bool = False

    def __init__(self, *args, **kwargs):
        BuildingBase.__init__(self, *args, **kwargs)

    def get_buttons(self) -> list[str]:
        buttons = BuildingBase.get_buttons(self)
        buttons.append("scrap")

        buttons.remove("store")

        return buttons
