from kivy.event import EventDispatcher
from kivy.properties import StringProperty, NumericProperty, BooleanProperty
from kivy3 import Renderer, Scene, Object3D

from lib.betterLogger import BetterLogger
from resources import Models
from graphics import graphicsConfig


class BuildingBase(EventDispatcher, BetterLogger):
    id = StringProperty(defaultvalue="None")
    obj: Object3D = None
    x: NumericProperty = NumericProperty(0)
    y: NumericProperty = NumericProperty(0)
    renderer: Renderer = None
    scene: Scene = None
    button_ids: list[str] = list()
    selected: BooleanProperty = BooleanProperty(False)

    def __init__(self, *args, **kwargs):
        BetterLogger.__init__(self)
        self.log_trace("Creating building with args", args, kwargs)
        self.id = kwargs.pop("id")
        self.on_building_id(self, self.id)

        EventDispatcher.__init__(self, *args, **kwargs)

        self.button_ids.extend(self.get_buttons())


    def on_building_id(self, instance, value):
        self.log_trace("building_id changed to", value)
        self.obj = Models.get(value)
        self.obj.pos.z = graphicsConfig.getint("BaseLayout", "building_start_z")

    def on_x(self, instance, value):
        self.obj.pos.x = value

    def on_y(self, instance, value):
        self.obj.pos.y = value

    def set_renderer_and_scene(self, renderer: Renderer, scene: Scene):
        self.renderer = renderer
        self.scene = scene

        self.scene.add(self.obj)
        self.renderer._instructions.add(self.obj.as_instructions())


    def get_buttons(self) -> list[str]:
        """
        Returns the button ids in a list of the buttons this building will show when clicked.
        This function will be overridden as different buildings need different buttons to do different things.
        """
        buttons: list[str] = list()
        buttons.append("info")

        return buttons


    def on_selected(self, instance, value):
        self.log_trace("Selected switched to", value, "on building", instance)

    def __repr__(self):
        base = str(object.__repr__(self))
        base = base.replace("<", "")
        base = base.replace(">", "")

        return "<'" + base + "' pos=" + str((self.x, self.y)) + \
               ", selected=" + str(self.selected) + ">"
