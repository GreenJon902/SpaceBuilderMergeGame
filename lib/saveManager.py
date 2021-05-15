# noinspection PyProtectedMember
from kivy._clock import ClockEvent
from kivy.clock import Clock
from kivy.event import EventDispatcher

from configurables import userSettings, gameData
from lib.betterLogger import BetterLogger


class _SaveManager(EventDispatcher, BetterLogger):
    __log_name__ = "SaveManager"

    save_clock: ClockEvent = None

    _game_data_updaters: list[callable] = list()

    def __init__(self):
        EventDispatcher.__init__(self)
        BetterLogger.__init__(self)

    def setup(self):
        pass

    def start_clock(self):
        self.save_clock = Clock.schedule_interval(lambda _elapsed_time: self.tick(),
                                                  userSettings.getint("time_between_save"))
        self.log_info("Clock started")

    def end_clock(self):
        self.save_clock.cancel()
        self.tick()
        self.log_info("Clock stopped")

    def tick(self):
        self.log_debug("Getting info to save for gameData")

        for updater in self._game_data_updaters:
            updater()


        self.log_debug("Getting info to save for userSettings")


        self.log_info("Saving...")

        gameData.save()
        userSettings.save()

        self.log_info("Saved")

    def register_update_game_data_function(self, function: callable):
        self._game_data_updaters.append(function)


SaveManager: _SaveManager = _SaveManager()
