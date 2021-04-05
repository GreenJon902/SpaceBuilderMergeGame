from kivy.app import App

from Graphics.spaceBuilderMergeGameScreenManager import SpaceBuilderMergeGameScreenManager


class SpaceBuilderMergeGameApp(App):
    def build(self):
        return SpaceBuilderMergeGameScreenManager()