from kivy.event import EventDispatcher
from kivy.properties import StringProperty, NumericProperty
from kivy3 import Object3D

from lib.betterLogger import BetterLogger
from resources import Models
from graphics import graphicsConfig


class BuildingBase(EventDispatcher, BetterLogger):
    building_id = StringProperty(defaultvalue="drill")
    obj: Object3D = None
    x: NumericProperty = NumericProperty(0)
    y: NumericProperty = NumericProperty(0)

    def __init__(self, *args, **kwargs):
        BetterLogger.__init__(self)
        self.log_trace("Creating building with args", args, kwargs)
        self.on_building_id(self, self.building_id)

        EventDispatcher.__init__(self, *args, **kwargs)


    def on_building_id(self, instance, value):
        self.log_trace("building_id changed to", value)
        self.obj = Models.get(value)
        self.obj.pos.z = graphicsConfig.getint("BaseLayout", "building_start_z")

    def on_x(self, instance, value):
        self.obj.pos.x = value

    def on_y(self, instance, value):
        self.obj.pos.y = value

