from kivy.uix.screenmanager import ScreenManager

from misc.betterLogger import BetterLogger


class SpaceBuilderMergeGameScreenManager(ScreenManager, BetterLogger):
    def set_screen(self, screen_name):
        self.current = screen_name

        self.log_info("Switched to " + str(screen_name))

