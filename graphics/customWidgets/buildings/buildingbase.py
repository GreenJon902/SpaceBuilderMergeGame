import os.path

from kivy.event import EventDispatcher
from kivy.properties import StringProperty
from kivy3 import Object3D, Material, Mesh
from kivy3.extras.geometries import BoxGeometry
from kivy3.loaders import OBJLoader, STLLoader, OBJMTLLoader

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
        path2 = os.path.join(AppInfo.resources_dir, "Models", "Buildings", str(value) + ".mtl")

        loader = OBJMTLLoader()
        print("path -", path)
        cube_geo = BoxGeometry(1, 1, 1)
        cube_mat = Material()

        self.obj = loader.load(path, path2)
        obj = Mesh(
            geometry=cube_geo,
            material=cube_mat
        )  # default pos == (0, 0, 0)
        self.obj.pos.z = -20
        self.obj.rotation.x = 90
        print(self.obj)
        print(self.obj.__dict__)

    def on_add(self):
        pass

