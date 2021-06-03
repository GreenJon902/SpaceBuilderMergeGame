from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, NoTransition, TransitionBase, Screen

from graphics import graphicsConfig
from lib.betterLogger import BetterLogger
from resources import Audio


class SpaceBuilderMergeGameScreenManager(ScreenManager, BetterLogger):
    def __init__(self, **kwargs):
        BetterLogger.__init__(self)
        ScreenManager.__init__(self, **kwargs)

        self.log_info("Using NoTransition")
        self.transition: TransitionBase = NoTransition()
        self.transition.duration = 0

        Audio.loop("main_theme")


    def set_screen(self, screen_name: str):
        if isinstance(self.transition, TransitionBase):
            self.log_info("Using", graphicsConfig.get("General", "transition"))
            self.transition: TransitionBase = graphicsConfig.getkivytranition("General", "transition")
            self.transition.duration = graphicsConfig.getfloat("General", "transition_length")

        self.current: str = screen_name

        self.log_info("Switched to " + str(screen_name))
        App.get_running_app().on_screen_change(self.current_screen)


def get_sm() -> SpaceBuilderMergeGameScreenManager:
    BetterLogger().log_deep_debug("get_sm(): Returning screen manager")
    return App.get_running_app().root.current


def get_screen(screen_name: str) -> Screen:
    return get_sm().get_screen(screen_name)
