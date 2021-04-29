from kivy.event import EventDispatcher
from kivy.properties import StringProperty
from kivy3 import Object3D

from lib.betterLogger import BetterLogger
from resources import Models
from staticConfigurables import graphics


class BuildingBase(EventDispatcher, BetterLogger):
    building_id = StringProperty(defaultvalue="drill")
    obj: Object3D = None

    def __init__(self, *args, **kwargs):
        EventDispatcher.__init__(self, *args, **kwargs)
        BetterLogger.__init__(self)

        self.on_building_id(self, self.building_id)

    def on_building_id(self, instance, value):
        self.obj = Models.get(value)
        self.obj.pos.z = graphics.getint("BaseLayout", "building_start_z")


    def on_add(self):
        pass
