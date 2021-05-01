import os.path
import random
from pprint import pprint

from kivy.clock import Clock
from kivy.input.providers.mouse import MouseMotionEvent
from kivy.properties import ListProperty
from kivy.uix.floatlayout import FloatLayout
from kivy3 import Mesh, Scene, Renderer, Material, PerspectiveCamera
from kivy3.extras.geometries import BoxGeometry

import AppInfo
from configurables import gameData
from graphics.customWidgets.betterScatter import BetterScatter
from graphics.customWidgets.buildings import str_to_building
from lib.betterLogger import BetterLogger


class BaseLayout(FloatLayout, BetterLogger):
    renderer: Renderer = Renderer(shader_file=os.path.join(AppInfo.resources_dir, "shader.glsl"))
    scene: Scene = Scene()
    scatter_widget: BetterScatter = None
    camera: PerspectiveCamera = PerspectiveCamera(
        fov=75,  # distance from the screen
        aspect=0,  # "screen" ratio
        near=1,  # nearest rendered point
        far=150  # farthest rendered point
    )
    buildings: ListProperty = ListProperty()

    def _adjust_aspect(self, *args):
        rsize = self.renderer.size
        aspect = rsize[0] / float(rsize[1])
        self.renderer.camera.aspect = aspect

    def __init__(self, *args, **kwargs):
        BetterLogger.__init__(self)
        FloatLayout.__init__(self, *args, **kwargs)

        self.create_renderer()

        self.log_info("Created renderer, starting to create building objects")

        for building_info in gameData.get("placed_buildings"):
            building = str_to_building[building_info["id"]](**building_info)
            self.log_debug("Created building object for", building_info)
            self.add_building(building)

        self.log_info("Created objects")


    """def on_kv_post(self, base_widget):
        self.scatter_widget.bind(scale=self.on_scatter_transform_with_touch, pos=self.on_scatter_transform_with_touch,
                                 rotation=self.on_scatter_transform_with_touch)

    def on_scatter_transform_with_touch(self, instance: BetterScatter, value: MouseMotionEvent):
        print(self.scatter_widget.bbox)
        try:
            print("hi", self.camera._look_at)
            self.camera.look_at([self.scatter_widget.x * -1, self.scatter_widget.y * -1, -100])
        except KeyError:
            print("POO")"""



    def add_building(self, building):
        self.buildings.append(building)
        self.scene.add(building.obj)
        self.renderer._instructions.add(building.obj.as_instructions())


    def create_renderer(self):
        self.renderer.render(self.scene, self.camera)
        self.renderer.bind(size=self._adjust_aspect)
        self.add_widget(self.renderer)


    def create_cube(self):
        cube_geo = BoxGeometry(1, 1, 1)  #  BoxGeometry(random.randint(5, 15)/10, random.randint(5, 15)/10, random.randint(5, 15)/10)
        cube_mat = Material(color=(random.randint(0, 100)/100, random.randint(0, 100)/100, random.randint(0, 100)/100))
        cube = Mesh(
            geometry=cube_geo,
            material=cube_mat
        )
        cube.pos.z = -5
        cube.rotation.x = random.randint(0, 360)
        self.scene.add(cube)
        Clock.schedule_interval(lambda *args: self.rotate_cube(cube), .01)
        self.renderer._instructions.add(cube.as_instructions())
