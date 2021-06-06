from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    # noinspection PyProtectedMember
    from kivy._clock import ClockEvent


from kivy.clock import Clock
from kivy.properties import NumericProperty, StringProperty

from graphics.buildings.buildingbase import BuildingBase
from lib.globalEvents import GlobalEvents
from resources import GameConfig


class ResourceMiner(BuildingBase):
    mine_batch_clock: ClockEvent = None
    mine_batch_time: float = NumericProperty(1000)
    mine_batch_amount: int = NumericProperty(0)
    mine_item: str = StringProperty("None")

    def __init__(self, *args, **kwargs):
        self.mine_batch_time = kwargs.pop("mine_batch_time", GameConfig.getfloat("Buildings", "resource_miner",
                                                                                 self.__type__, "speed"))
        self.mine_batch_amount = kwargs.pop("mine_batch_amount", GameConfig.getint("Buildings", "resource_miner",
                                                                                     self.__type__, "amount"))
        self.mine_item = kwargs.pop("mine_item", GameConfig.get("Buildings", "resource_miner", self.__type__, "item"))

        BuildingBase.__init__(self, *args, **kwargs)

        self.mine_batch_clock = Clock.schedule_interval(lambda _elapsed_time: self.mine_batch_finished(),
                                                            self.mine_batch_time)

    def mine_batch_finished(self):
        self.log_deep_debug("Finished mining batch of", self.mine_batch_amount, self.mine_item)

        GlobalEvents.dispatch("mine_batch_finished", self)

    def on_mine_batch_time(self, _instance, value: float):
        self.mine_batch_clock.cancel()
        self.mine_batch_clock = Clock.schedule_interval(lambda _elapsed_time: self.mine_batch_finished(),
                                                            value)


__all__ = ["ResourceMiner"]
