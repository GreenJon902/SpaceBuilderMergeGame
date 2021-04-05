from kivy.app import App

from Graphics.spaceBuilderMergeGameScreenManager import SpaceBuilderMergeGameScreenManager
from misc.betterLogger import BetterLogger


class SpaceBuilderMergeGameApp(App, BetterLogger):
    def build(self):
        self.log_info("Building app")

        return SpaceBuilderMergeGameScreenManager()
