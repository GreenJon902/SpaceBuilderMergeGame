from kivy.uix.screenmanager import Screen

from lib.betterLogger import BetterLogger


class ShopScreen(Screen, BetterLogger):
    def __init__(self, **kwargs):
        BetterLogger.__init__(self)
        Screen.__init__(self, **kwargs)
