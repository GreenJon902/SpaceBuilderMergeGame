import os

from kivy.logger import Logger
from kivy.factory import Factory
from kivy.lang import Builder

import AppInfo
from Graphics.spaceBuilderMergeGameApp import SpaceBuilderMergeGameApp


def load_kv():
    for filename in os.listdir(AppInfo.kv_language_dir):
        Logger.debug("kv_loader: Loading " + str(filename))
        Builder.load_file(os.path.join(AppInfo.kv_language_dir, filename))
        Logger.debug("kv_loader: Loaded " + str(filename))


def setup():
    from Graphics.Screens.exampleScreen import ExampleScreen
    from Graphics.spaceBuilderMergeGameScreenManager import SpaceBuilderMergeGameScreenManager


    Factory.register("DrawSwapScreenManager", cls=SpaceBuilderMergeGameScreenManager)
    Factory.register("ExampleScreen", cls=ExampleScreen)

    Logger.info("All classes have been assigned to Factory")


def start():
    Logger.info("Graphics are starting")

    app = SpaceBuilderMergeGameApp()
    app.run()

    Logger.info("Graphics have ended")
