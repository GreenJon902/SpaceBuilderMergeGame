from kivy.uix.screenmanager import ScreenManager


class [AppName]ScreenManager(ScreenManager, BetterLogger):
    def set_screen(self, screen_name):
        self.current = screen_name

        self.log_info("Switched to " + str(screen_name))

