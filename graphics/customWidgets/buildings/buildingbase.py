from kivy.clock import Clock
from kivy.event import EventDispatcher
from kivy.graphics.transformation import Matrix
from kivy.properties import StringProperty, NumericProperty, BooleanProperty
from kivy3 import Renderer, Scene, Object3D

from configurables import gameData
from graphics import graphicsConfig, height, width
from graphics.spaceBuilderMergeGameScreenManager import get_screen
from lib.betterLogger import BetterLogger
from resources import Models


class BuildingBase(EventDispatcher, BetterLogger):
    id: str = StringProperty(defaultvalue="None")
    _obj: Object3D = None
    x: float = NumericProperty(0)
    y: float = NumericProperty(0)
    rotation: float = NumericProperty(0)
    renderer: Renderer = None
    scene: Scene = None
    selected: bool = BooleanProperty(False)
    parent = None
    movable: bool = True

    def __init__(self, *args, **kwargs):
        BetterLogger.__init__(self)
        self.log_trace("Creating building with args", args, kwargs)
        self.id = kwargs.pop("id")
        self.on_building_id(self, self.id)

        EventDispatcher.__init__(self, *args, **kwargs)


    def on_building_id(self, _instance, value):
        self.log_trace("building_id changed to", value)
        self._obj = Models.get(value)
        self._obj.pos.z = graphicsConfig.getint("BaseLayout", "building_start_z")

    def on_x(self, _instance, value):
        self._obj.pos.x = value

    def on_y(self, _instance, value):
        self._obj.pos.y = value

    def on_rotation(self, _instance, value):
        self._obj.rotation.z = value

    def set_renderer_and_scene(self, renderer: Renderer, scene: Scene):
        self.renderer = renderer
        self.scene = scene

        self.scene.add(self._obj)
        # noinspection PyProtectedMember
        self.renderer._instructions.add(self._obj.as_instructions())


    def get_buttons(self) -> list[str]:
        """
        Returns the button ids in a list of the buttons this building will show when clicked.
        This function will be overridden as different buildings need different buttons to do different things.
        """
        buttons: list[str] = list()
        buttons.append("info")
        buttons.append("store")

        return buttons

    @property
    def button_ids(self) -> list[str]:
        b_ids = self.get_buttons()

        self.log_trace("Getting buttons ids for", self, "got", b_ids)
        return b_ids


    def on_selected(self, instance, value: bool):
        self.log_trace("Selected switched to", value, "on building", instance)
        if value:
            get_screen("BaseBuildScreen").ids["building_buttons_handler"].redo_buttons(self.button_ids, self)

    def __repr__(self) -> str:
        base = str(object.__repr__(self))
        base = base.replace("<", "")
        base = base.replace(">", "")

        return "<'" + base + "' pos=" + str((self.x, self.y)) + \
               ", selected=" + str(self.selected) + ">"


    def store(self):
        self.log_debug("Storing self -", self)

        # noinspection PyProtectedMember
        self._obj._instructions.clear()
        # noinspection PyProtectedMember
        self.renderer._instructions.remove(self._obj.as_instructions())

        self.scene.children.remove(self._obj)
        self.selected = False

        self.parent.buildings.remove(self)
        get_screen("BaseBuildScreen").ids["building_buttons_handler"].clear_buttons()

        self.parent = None

        get_screen("BaseBuildScreen").ids["scatter"].rotation += 0.001

        Clock.schedule_once(un_turn, 0)

        gameData.add_to_inventory(self.id, 1)


    def get_projected_corners(self) -> tuple[tuple[int, int], tuple[int, int]]:
        m = Matrix()
        x, y, z = m.project(self._obj.pos[0] - 5, self._obj.pos[1] - 5, self._obj.pos[2] - 5,
                            self.parent.camera.model_matrix, self.parent.camera.projection_matrix,
                            self.parent.camera.pos.x, self.parent.camera.pos.y, width(), height())

        x2, y2, z2 = m.project(self._obj.pos[0] + 5, self._obj.pos[1] + 5, self._obj.pos[2],
                               self.parent.camera.model_matrix, self.parent.camera.projection_matrix,
                               self.parent.camera.pos.x, self.parent.camera.pos.y, width(), height())

        return (x, y), (x2, y2)

    def get_projected_origin(self) -> tuple[int, int]:
        m = Matrix()
        x, y, z = m.project(self._obj.pos[0], self._obj.pos[1], self._obj.pos[2],
                            self.parent.camera.model_matrix, self.parent.camera.projection_matrix,
                            self.parent.camera.pos.x, self.parent.camera.pos.y, width(), height())

        return x, y


# A rather hacky fix to update the canvas, I don't exactly know how the kivy and kivy3 drawing works so i went with this
def un_turn(_elapsed_time: int):
    get_screen("BaseBuildScreen").ids["scatter"].rotation -= 0.001
