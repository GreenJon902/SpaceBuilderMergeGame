import os

from kivy.logger import Logger
from kivy.factory import Factory
from kivy.lang import Builder

import AppInfo
from Graphics.[AppName] import [AppName]


def load_kv():
    for filename in os.listdir(AppInfo.kv_language_dir):
        Logger.debug("kv_loader: Loading " + str(filename))
        Builder.load_file(os.path.join(AppInfo.kv_language_dir, filename))
        Logger.debug("kv_loader: Loaded " + str(filename))


def setup():
    from Graphics.Screens.exampleScreen import ExampleScreen


    Factory.register("DrawSwapScreenManager", cls=[AppName]ScreenManager)
    Factory.register("ExampleScreen", cls=ExampleScreen)

    Logger.info("All classes have been assigned to Factory")


def start():
    Logger.info("Graphics are starting")

    app = [AppName]()
    app.run()

    Logger.info("Graphics have ended")
