import os.path

from kivy.event import EventDispatcher
from kivy.properties import StringProperty
from kivy3 import Object3D, Mesh
from lib.betterKv3 import OBJLoader

import AppInfo
from lib.betterLogger import BetterLogger


class BuildingBase(EventDispatcher, BetterLogger):
    building_id = StringProperty(defaultvalue="drill")
    obj: Object3D = None

    def __init__(self, *args, **kwargs):
        EventDispatcher.__init__(self, *args, **kwargs)
        BetterLogger.__init__(self)

        self.on_building_id(self, self.building_id)

    def on_building_id(self, instance, value):
        path = os.path.join(AppInfo.resources_dir, "Models", "Buildings", str(value) + ".obj")

        loader = OBJLoader()

        self.obj = loader.load(path)
        self.obj.pos.z = -20
        self.obj.rotation.x = 90


    def on_add(self):
        pass
