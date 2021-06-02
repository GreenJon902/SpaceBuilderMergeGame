from graphics.buildings.buildingbase import BuildingBase


class Drill(BuildingBase):
    __type__: str = "drill"

    def __init__(self, *args, **kwargs):
        BuildingBase.__init__(self, *args, **kwargs)
