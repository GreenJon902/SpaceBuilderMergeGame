from kivy.app import App
from kivy.factory import Factory

from graphics.spaceBuilderMergeGameScreenManager import SpaceBuilderMergeGameScreenManager
from lib.betterLogger import BetterLogger
from resources import Lang


class SpaceBuilderMergeGameApp(App, BetterLogger):
    def build(self) -> SpaceBuilderMergeGameScreenManager:
        self.log_info("Building app")

        sm: SpaceBuilderMergeGameScreenManager = Factory.SpaceBuilderMergeGameScreenManager()
        sm.bind(on_current=self.on_screen_change)

        return sm

    def on_screen_change(self, new_screen: str):
        self.title = Lang.get("General.Title") + " - " + str(new_screen.name)
