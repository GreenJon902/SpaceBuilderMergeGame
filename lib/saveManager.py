from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    # noinspection PyProtectedMember
    from kivy._clock import ClockEvent


# noinspection PyProtectedMember
from threading import Thread

from kivy.clock import Clock
from kivy.event import EventDispatcher

from configurables import userSettings, gameData
from lib.betterLogger import BetterLogger


class _SaveManager(EventDispatcher, BetterLogger):
    tick_logger = BetterLogger(name="SaveManager_tick() | ")

    save_clock: ClockEvent = None

    _game_data_updaters: list[callable] = list()

    def __init__(self):
        EventDispatcher.__init__(self)
        BetterLogger.__init__(self, name="SaveManager")

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
        t = Thread(target=self._tick)
        self.log_deep_debug("Created thread -", t, " Starting now")
        self.tick_logger.__log_name_suffix__ = str(t.getName())
        t.start()

    def _tick(self):
        logger = self.tick_logger

        logger.log_debug("Getting info to save for gameData")

        for updater in self._game_data_updaters:
            updater()

        logger.log_debug("Getting info to save for userSettings")

        logger.log_info("Saving...")

        gameData.save()
        userSettings.save()

        logger.log_info("Saved")



    def register_update_game_data_function(self, function: callable):
        self._game_data_updaters.append(function)
        self.log_deep_debug("Registered save function -", function)

    def un_register_update_game_data_function(self, function: callable):
        self._game_data_updaters.remove(function)
        self.log_deep_debug("Unregistered save function -", function)


SaveManager: _SaveManager = _SaveManager()


__all__ = ["SaveManager"]
