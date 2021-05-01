from kivy.event import EventDispatcher
from kivy.properties import StringProperty, NumericProperty
from kivy3 import Object3D

from lib.betterLogger import BetterLogger
from resources import Models
from staticConfigurables import graphicsConfig


class BuildingBase(EventDispatcher, BetterLogger):
    building_id = StringProperty(defaultvalue="drill")
    obj: Object3D = None
    x: NumericProperty = NumericProperty(0)
    y: NumericProperty = NumericProperty(0)

    def __init__(self, *args, **kwargs):
        EventDispatcher.__init__(self, *args, **kwargs)
        BetterLogger.__init__(self)

        self.on_building_id(self, self.building_id)

    def on_building_id(self, instance, value):
        self.obj = Models.get(value)
        self.obj.pos.z = graphicsConfig.getint("BaseLayout", "building_start_z")


    def move_to(self, new_pos):
        self.obj.pos.x = new_pos[0]
        self.obj.pos.y = new_pos[1]
