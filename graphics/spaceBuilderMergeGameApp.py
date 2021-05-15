from kivy.app import App
from kivy.factory import Factory
from kivy.uix.screenmanager import Screen

from graphics.spaceBuilderMergeGameScreenManager import SpaceBuilderMergeGameScreenManager
from lib.betterLogger import BetterLogger
from lib.saveManager import SaveManager
from resources import Lang


class SpaceBuilderMergeGameApp(App, BetterLogger):
    sm: SpaceBuilderMergeGameScreenManager = None

    def on_sm(self):
        self.sm.bind(on_current=self.on_screen_change)

    def build(self) -> SpaceBuilderMergeGameScreenManager:
        self.log_info("Building app")

        return Factory.ScreenManagerSwitcher()

    def on_screen_change(self, new_screen: Screen):
        self.title = Lang.get("General.Title") + " - " + str(new_screen.name)

    def on_stop(self):
        SaveManager.end_clock()

    def on_start(self):
        SaveManager.start_clock()
