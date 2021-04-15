import os

from kivy.logger import Logger
from kivy.factory import Factory
from kivy.lang import Builder

import AppInfo


def load_kv():
    for filename in os.listdir(AppInfo.kv_language_dir):
        Logger.debug("kv_loader: Loading " + str(filename))
        Builder.load_file(os.path.join(AppInfo.kv_language_dir, filename))
        Logger.debug("kv_loader: Loaded " + str(filename))


def setup():
    from Graphics.spaceBuilderMergeGameApp import SpaceBuilderMergeGameApp
    from Graphics.spaceBuilderMergeGameScreenManager import SpaceBuilderMergeGameScreenManager
    from Graphics.Screens.baseBuildScreen import BaseBuildScreen


    Factory.register("SpaceBuilderMergeGameApp",
                     cls=SpaceBuilderMergeGameApp,
                     module="Graphics.spaceBuilderMergeGameApp")

    Factory.register("DrawSwapScreenManager",
                     cls=SpaceBuilderMergeGameScreenManager,
                     module="Graphics.SpaceBuilderMergeGameScreenManager")

    Factory.register("BaseBuildScreen",
                     cls=BaseBuildScreen,
                     module="Graphics.Screens.baseBuildScreen")


    Logger.info("All classes have been assigned to Factory")


def start():
    Logger.info("Graphics are starting")

    app = Factory.SpaceBuilderMergeGameApp()
    app.run()

    Logger.info("Graphics have ended")
