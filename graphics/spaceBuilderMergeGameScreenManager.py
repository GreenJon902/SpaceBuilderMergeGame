from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, NoTransition, TransitionBase

from lib.betterLogger import BetterLogger


class SpaceBuilderMergeGameScreenManager(ScreenManager, BetterLogger):
    def __init__(self, *args: any, **kwargs):
        super(SpaceBuilderMergeGameScreenManager, self).__init__(*args, **kwargs)

        self.log_info("ScreenManager: Using FadeTransition")
        self.transition: TransitionBase = NoTransition()

        self.set_screen("SplashScreen2")

    def set_screen(self, screen_name: str):
        self.current: str = screen_name

        self.log_info("Switched to " + str(screen_name))


def get_sm() -> SpaceBuilderMergeGameScreenManager:
    BetterLogger().log_trace("get_sm(): Returning screen manager")
    return App.get_running_app().root
