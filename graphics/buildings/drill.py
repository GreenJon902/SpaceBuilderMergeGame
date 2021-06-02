from graphics.buildings.resourceMiner import ResourceMiner


class Drill(ResourceMiner):
    __type__: str = "drill"

    def __init__(self, *args, **kwargs):
        ResourceMiner.__init__(self, *args, **kwargs)
