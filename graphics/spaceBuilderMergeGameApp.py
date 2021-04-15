from kivy.app import App
from kivy.factory import Factory

from lib.betterLogger import BetterLogger


class SpaceBuilderMergeGameApp(App, BetterLogger):
    def build(self):
        self.log_info("Building app")

        return Factory.SpaceBuilderMergeGameScreenManager()
