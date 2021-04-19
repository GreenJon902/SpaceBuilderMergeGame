import ntpath
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


def load_pre_load_kv():
    path: str = AppInfo.pre_load_kv_lang_path
    Logger.debug("kv_loader: Loading " + str(ntpath.basename(path)))
    Builder.load_file(path)
    Logger.debug("kv_loader: Loaded " + str(ntpath.basename(path)))


def setup():
    from graphics.spaceBuilderMergeGameApp import SpaceBuilderMergeGameApp
    from graphics.customWidgets.screenManagerSwitcher import ScreenManagerSwitcher
    from graphics.preLoadScreenManager import PreLoadScreenManager
    from graphics.spaceBuilderMergeGameScreenManager import SpaceBuilderMergeGameScreenManager
    from graphics.screens.splashScreen1 import SplashScreen1
    from graphics.screens.splashScreen2 import SplashScreen2
    from graphics.screens.loadingScreen import LoadingScreen
    from graphics.screens.baseBuildScreen import BaseBuildScreen
    from graphics.customWidgets.multiLangLabel import MultiLangLabel
    from graphics.customWidgets.baseLayout import BaseLayout

    Factory.register("SpaceBuilderMergeGameApp",
                     cls=SpaceBuilderMergeGameApp,
                     module="graphics.spaceBuilderMergeGameApp")

    Factory.register("SpaceBuilderMergeGameScreenManager",
                     cls=SpaceBuilderMergeGameScreenManager,
                     module="graphics.SpaceBuilderMergeGameScreenManager")

    Factory.register("PreLoadScreenManager",
                     cls=PreLoadScreenManager,
                     module="graphics.preLoadScreenManager")

    Factory.register("SplashScreen1",
                     cls=SplashScreen1,
                     module="graphics.screens.splashScreen")

    Factory.register("SplashScreen2",
                     cls=SplashScreen2,
                     module="graphics.screens.splashScreen")

    Factory.register("LoadingScreen",
                     cls=LoadingScreen,
                     module="graphics.screens.loadingScreen")

    Factory.register("BaseBuildScreen",
                     cls=BaseBuildScreen,
                     module="graphics.screens.baseBuildScreen")

    Factory.register("MultiLangLabel",
                     cls=MultiLangLabel,
                     module="graphics.customWidget.multiLangLabel")

    Factory.register("BaseLayout",
                     cls=BaseLayout,
                     module="graphics.customWidget.baseLayout")

    Logger.info("All classes have been assigned to Factory")


def start():
    Logger.info("graphics are starting")
    from graphics.spaceBuilderMergeGameApp import SpaceBuilderMergeGameApp

    app: SpaceBuilderMergeGameApp = Factory.SpaceBuilderMergeGameApp()
    app.run()

    Logger.info("graphics have ended")
