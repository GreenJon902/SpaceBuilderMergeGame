from kivy.app import App
from kivy.uix import screenmanager
from kivy.uix.screenmanager import ScreenManager

import staticConfigurables
from lib.betterLogger import BetterLogger


class SpaceBuilderMergeGameScreenManager(ScreenManager, BetterLogger):
    def __init__(self, *args, **kwargs):
        super(SpaceBuilderMergeGameScreenManager, self).__init__(*args, **kwargs)

        self.log_info("ScreenManager: Using" + str(staticConfigurables.graphics.get("General", "transition")))
        self.transition = screenmanager.__dict__[str(staticConfigurables.graphics.get("General", "transition"))]()

        self.set_screen(str(staticConfigurables.graphics.get("General", "start_screen")))

    def set_screen(self, screen_name):
        self.current = screen_name

        self.log_info("Switched to " + str(screen_name))
        App.get_running_app().on_screen_change(self.current_screen)


