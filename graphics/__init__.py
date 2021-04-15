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
    from graphics.spaceBuilderMergeGameApp import SpaceBuilderMergeGameApp
    from graphics.spaceBuilderMergeGameScreenManager import SpaceBuilderMergeGameScreenManager
    from graphics.screens.baseBuildScreen import BaseBuildScreen
    from graphics.customWidgets.multiLangLabel import MultiLangLabel


    Factory.register("SpaceBuilderMergeGameApp",
                     cls=SpaceBuilderMergeGameApp,
                     module="graphics.spaceBuilderMergeGameApp")

    Factory.register("DrawSwapScreenManager",
                     cls=SpaceBuilderMergeGameScreenManager,
                     module="graphics.SpaceBuilderMergeGameScreenManager")

    Factory.register("BaseBuildScreen",
                     cls=BaseBuildScreen,
                     module="graphics.screens.baseBuildScreen")

    Factory.register("MultiLangLabel",
                     cls=MultiLangLabel,
                     module="graphics.customWidget.multiLangLabel")


    Logger.info("All classes have been assigned to Factory")


def start():
    Logger.info("graphics are starting")

    app = Factory.SpaceBuilderMergeGameApp()
    app.run()

    Logger.info("graphics have ended")
