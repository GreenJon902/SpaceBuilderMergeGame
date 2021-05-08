from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, NoTransition, TransitionBase, Screen

from lib.betterLogger import BetterLogger


class SpaceBuilderMergeGameScreenManager(ScreenManager, BetterLogger):
    def __init__(self, **kwargs):
        BetterLogger.__init__(self)
        ScreenManager.__init__(self, **kwargs)

        self.log_info("ScreenManager: Using FadeTransition")
        self.transition: TransitionBase = NoTransition()


    def set_screen(self, screen_name: str):
        self.current: str = screen_name

        self.log_info("Switched to " + str(screen_name))
        App.get_running_app().on_screen_change(self.current_screen)


def get_sm() -> SpaceBuilderMergeGameScreenManager:
    BetterLogger().log_trace("get_sm(): Returning screen manager")
    return App.get_running_app().root.current


def get_screen(screen_name: str) -> Screen:
    return get_sm().get_screen(screen_name)
