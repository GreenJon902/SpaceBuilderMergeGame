from kivy.clock import Clock
from kivy.uix.floatlayout import FloatLayout
from kivy3 import Renderer, Scene, Material, Mesh, PerspectiveCamera
from kivy3.extras.geometries import BoxGeometry

from lib.betterLogger import BetterLogger


class BaseLayout(FloatLayout, BetterLogger):
    def _adjust_aspect(self, *args):
        rsize = self.renderer.size
        aspect = rsize[0] / float(rsize[1])
        self.renderer.camera.aspect = aspect

    def __init__(self, *args, **kwargs):
        BetterLogger.__init__(self)
        FloatLayout.__init__(self, *args, **kwargs)

        layout = FloatLayout()

        # create renderer
        self.renderer = Renderer()

        # create scene
        scene = Scene()

        # create default cube for scene
        cube_geo = BoxGeometry(1, 1, 1)
        cube_mat = Material()
        self.cube = Mesh(
            geometry=cube_geo,
            material=cube_mat
        )
        self.cube.pos.z = -5

        # create camera for scene
        self.camera = PerspectiveCamera(
            fov=75,  # distance from the screen
            aspect=0,  # "screen" ratio
            near=1,  # nearest rendered point
            far=10  # farthest rendered point
        )

        # start rendering the scene and camera
        scene.add(self.cube)
        self.renderer.render(scene, self.camera)

        # set renderer ratio is its size changes
        # e.g. when added to parent
        self.renderer.bind(size=self._adjust_aspect)

        layout.add_widget(self.renderer)
        self.add_widget(layout)
