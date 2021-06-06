from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from kivy.uix.screenmanager import TransitionBase


from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, NoTransition, TransitionBase

from lib.betterLogger import BetterLogger


class PreLoadScreenManager(ScreenManager, BetterLogger):
    def __init__(self, **kwargs):
        BetterLogger.__init__(self)
        ScreenManager.__init__(self, **kwargs)

        self.log_info("Using NoTransition")
        self.transition: TransitionBase = NoTransition()

        self.set_screen("LoadingScreen")

    def set_screen(self, screen_name: str):
        self.current: str = screen_name

        self.log_info("Switched to " + str(screen_name))

    def add_screens(self):
        pass


def get_sm() -> PreLoadScreenManager:
    BetterLogger().log_deep_debug("get_sm(): Returning screen manager")
    return App.get_running_app().root.current


__all__ = ["PreLoadScreenManager", "get_sm"]
