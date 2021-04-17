from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, NoTransition

from lib.betterLogger import BetterLogger


class SpaceBuilderMergeGameScreenManager(ScreenManager, BetterLogger):
    def __init__(self, *args, **kwargs):
        super(SpaceBuilderMergeGameScreenManager, self).__init__(*args, **kwargs)

        self.log_info("ScreenManager: Using FadeTransition")
        self.transition = NoTransition()

        self.set_screen("SplashScreen1")

    def set_screen(self, screen_name):
        self.current = screen_name

        self.log_info("Switched to " + str(screen_name))


def get_sm():
    BetterLogger.log_trace("get_sm(): Returning screen manager")
    return App.get_running_app().root
