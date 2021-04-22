import random

from kivy.clock import Clock
from kivy.uix.floatlayout import FloatLayout
from kivy3 import Mesh, Scene, Renderer, Material, PerspectiveCamera
from kivy3.extras.geometries import BoxGeometry

from lib.betterLogger import BetterLogger


class BaseLayout(FloatLayout, BetterLogger):
    renderer = Renderer()
    scene = Scene()
    camera = PerspectiveCamera(
        fov=75,  # distance from the screen
        aspect=0,  # "screen" ratio
        near=1,  # nearest rendered point
        far=10  # farthest rendered point
    )

    def _adjust_aspect(self, *args):
        rsize = self.renderer.size
        aspect = rsize[0] / float(rsize[1])
        self.renderer.camera.aspect = aspect

    def rotate_cube(self, cube):
        cube.rotation.x += random.randint(-10, 10)
        cube.rotation.y += random.randint(-10, 10)
        cube.rotation.z += random.randint(-10, 10)

    def __init__(self, *args, **kwargs):
        BetterLogger.__init__(self)
        FloatLayout.__init__(self, *args, **kwargs)

        self.create_renderer()
        Clock.schedule_interval(lambda *args: self.create_cube(), 0)


    def create_renderer(self):
        self.renderer.render(self.scene, self.camera)
        self.renderer.bind(size=self._adjust_aspect)
        self.add_widget(self.renderer)


    def create_cube(self):
        cube_geo = BoxGeometry(random.randint(5, 15)/10, random.randint(5, 15)/10, random.randint(5, 15)/10)
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
