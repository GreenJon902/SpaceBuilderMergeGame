import os.path
import random
from math import atan

from kivy.clock import Clock
from kivy.graphics.transformation import Matrix
from kivy.graphics import Color, Rectangle
from kivy.input import MotionEvent
from kivy.properties import ListProperty
from kivy.uix.floatlayout import FloatLayout
from kivy3 import Mesh, Scene, Renderer, Material, PerspectiveCamera
from kivy3.extras.geometries import BoxGeometry

import AppInfo
from configurables import gameData
from graphics import width, height
from graphics.betterKv3.vectors import Vector3
from graphics.customWidgets.betterScatter import BetterScatter
from graphics.customWidgets.buildings import str_to_building
from graphics.customWidgets.buildings.buildingbase import BuildingBase
from lib.betterLogger import BetterLogger


class BaseLayout(FloatLayout, BetterLogger):
    last_touch_pos: tuple[int, int] = [0, 0]
    renderer: Renderer = Renderer(shader_file=os.path.join(AppInfo.resources_dir, "shader.glsl"))
    scene: Scene = Scene()
    scatter_widget: BetterScatter = None
    camera: PerspectiveCamera = PerspectiveCamera(
        fov=75,  # distance from the screen
        aspect=0,  # "screen" ratio
        near=1,  # nearest rendered point
        far=150  # farthest rendered point
    )
    buildings: list[BuildingBase] = ListProperty()

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
            building_class = str_to_building[building_info["id"]]
            building = building_class(**building_info)

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
        building.set_renderer_and_scene(self.renderer, self.scene)
        self.buildings.append(building)

    def create_renderer(self):
        self.renderer.render(self.scene, self.camera)
        self.renderer.bind(size=self._adjust_aspect)
        self.add_widget(self.renderer)

    def create_cube(self):
        cube_geo = BoxGeometry(1, 1, 1)
        #  BoxGeometry(random.randint(5, 15)/10, random.randint(5, 15)/10, random.randint(5, 15)/10)
        cube_mat = Material(
            color=(random.randint(0, 100) / 100, random.randint(0, 100) / 100, random.randint(0, 100) / 100))
        cube = Mesh(
            geometry=cube_geo,
            material=cube_mat
        )
        cube.pos.z = -5
        cube.rotation.x = random.randint(0, 360)
        self.scene.add(cube)
        Clock.schedule_interval(lambda *args: self.rotate_cube(cube), .01)
        self.renderer._instructions.add(cube.as_instructions())

    def on_touch_down(self, touch: MotionEvent):
        if touch.is_touch:
            self.last_touch_pos = touch.pos

    def on_touch_up(self, touch: MotionEvent):
        if touch.is_touch:
            to_select: BuildingBase = None

            building: BuildingBase
            for building in self.buildings:
                # I want my long time and effort to be remembered, this to so long, AND THE ANSWER WAS SO SIMPLE OMG
                """bPos = building.obj.pos[0], building.obj.pos[1],  building.obj.pos[2]
                bPos2 = building.obj.pos[0] + self.renderer.width, building.obj.pos[1] + self.renderer.height, building.obj.pos[2]
                cPos = self.camera.pos"""

                """bVPos = Vector3(bPos)
                bVPos2 = Vector3(bPos2)
                x, y, z = bVPos + Vector3(0, 0, 100)
                x2, y2, z2 = bVPos2 + Vector3(0, 0, 100)
                print(x, y, z, x2, y2, z2)"""

                """pitch = atan((bPos[0] - cPos.x) / (bPos[1] - cPos.y))
                yaw = atan((bPos[2] - cPos.z) / (bPos[1] - cPos.y))
    
                x = width() / 2 + (pitch * (width() / self.camera.fov))
                y = height() / 2 + (yaw * (height() / self.camera.fov))
    
    
                pitch2 = atan((bPos2[0] - cPos.x) / (bPos2[1] - cPos.y))
                yaw2 = atan((bPos2[2] - cPos.z) / (bPos2[1] - cPos.y))
    
                x2 = width() / 2 + (pitch2 * (width() / self.camera.fov))
                y2 = height() / 2 + (yaw2 * (height() / self.camera.fov))
    
                print(touch.x, touch.y)
                print(bPos, bPos2, cPos)
                print(x, y, x2, y2)
                print(self.camera.rotation)"""

                """print(building)
                print(building.obj.pos, building.obj.scale)
                print(building.obj._instructions, building.obj._instructions.children)
                print()
                print()
                print(building.obj._translate.matrix)
                print()
                print()
                print(building.obj._scale.matrix)
                print()
                print()
                print(building.obj._rotors["x"].matrix)
                print()
                print(building.obj._rotors["y"].matrix)
                print()
                print(building.obj._rotors["z"].matrix)"""
                """print(building.obj.pos, (building.obj.pos[0] - (width() / 2), building.obj.pos[1] - (height() / 2)), building.obj.scale.xyz)
                print(touch.pos)
                print(touch.pos[0] - (width() / 2), touch.pos[1] - (height() / 2))
                print(self.renderer.size)
                print(self.scatter_widget.scale)
                print(Vector3.get_XY_from_camera(building.obj.pos, self.camera))
                print()
                print()
                print()
                print()
                print(Matrix())
                print(Matrix().project(building.obj.pos[0], building.obj.pos[1], building.obj.pos[2], Matrix(), Matrix(), self.camera.pos.x, self.camera.pos.y, width(), height()))"""

                m = Matrix()
                x, y, z2 = m.project(building.obj.pos[0]-5, building.obj.pos[1]-5, building.obj.pos[2]-5,
                                       self.camera.model_matrix, self.camera.projection_matrix,
                                       self.camera.pos.x, self.camera.pos.y, width(), height())

                x2, y2, z2 = m.project(building.obj.pos[0]+5, building.obj.pos[1]+5, building.obj.pos[2],
                                       self.camera.model_matrix, self.camera.projection_matrix,
                                       self.camera.pos.x, self.camera.pos.y, width(), height())


                # Will leave here for debug
                """with self.canvas.after:
                    Color(rgba=(0, 1, 0, 0.5))
    
                    Rectangle(pos=(x, y), size=(x2 - x, y2 - y))"""

                if x <= touch.x <= x2 and y <= touch.y <= y2:
                    self.log_debug("Building", building, "was clicked on, setting building to selected and grabbing touch")
                    to_select = building
                    break

            if to_select is None:
                self.log_trace("User touched but no building was clicked, ignoring touch")


            else:
                buildings = self.buildings.copy()
                buildings.remove(to_select)

                for building in buildings:
                    building.selected = False

                to_select.selected = True
