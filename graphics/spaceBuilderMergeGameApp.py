from kivy.app import App
from kivy.factory import Factory

from lib.betterLogger import BetterLogger
from resources import Lang


class SpaceBuilderMergeGameApp(App, BetterLogger):
    def build(self):
        self.log_info("Building app")

        sm = Factory.SpaceBuilderMergeGameScreenManager()
        sm.bind(on_current=self.on_screen_change)

        return sm

    def on_screen_change(self, new_screen):
        self.title = Lang.get("General.Title") + " - " + str(new_screen.name)
