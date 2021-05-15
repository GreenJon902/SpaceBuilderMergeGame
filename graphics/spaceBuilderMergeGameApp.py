from kivy.app import App
from kivy.factory import Factory
from kivy.uix.screenmanager import Screen

from configurables import gameData, userSettings
from graphics.spaceBuilderMergeGameScreenManager import SpaceBuilderMergeGameScreenManager
from lib.betterLogger import BetterLogger
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
        self.log_info("Starting saving -", gameData, ",", userSettings)
        gameData.save()
        userSettings.save()
        self.log_info("Saved!")
