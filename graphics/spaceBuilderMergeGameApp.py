from kivy.app import App
from kivy.factory import Factory
from kivy.properties import StringProperty

from lib.betterLogger import BetterLogger
from resources import Lang


class SpaceBuilderMergeGameApp(App, BetterLogger):
    def build(self):
        self.log_info("Building app")

        return Factory.SpaceBuilderMergeGameScreenManager()

    def on_screen_change(self, new_screen):
        self.title = Lang.get("General.Title") + " - " + str(new_screen.name)
