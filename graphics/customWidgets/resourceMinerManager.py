from kivy.uix.floatlayout import FloatLayout

from lib.betterLogger import BetterLogger


class ResourceMinerManager(FloatLayout, BetterLogger):
    def __init__(self, **kwargs):
        BetterLogger.__init__(self)
        FloatLayout.__init__(self, **kwargs)
