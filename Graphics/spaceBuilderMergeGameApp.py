from kivy.app import App
from kivy.factory import Factory

from misc.betterLogger import BetterLogger


class SpaceBuilderMergeGameApp(App, BetterLogger):
    def build(self):
        self.log_info("Building app")

        return Factory.SpaceBuilderMergeGameScreenManager()
