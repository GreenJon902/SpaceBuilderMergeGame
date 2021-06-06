from kivy.uix.floatlayout import FloatLayout

from configurables import gameData
from lib.betterLogger import BetterLogger
from lib.globalEvents import GlobalEvents


class ResourceMinerManager(FloatLayout, BetterLogger):
    def __init__(self, **kwargs):
        BetterLogger.__init__(self)
        FloatLayout.__init__(self, **kwargs)

        GlobalEvents.bind(mine_batch_finished=self.batch_finished)

    # noinspection PyMethodMayBeStatic
    # ignore because we will do something else with this later
    def batch_finished(self, resourceMiner: "ResourceMiner"):
        gameData.add_to_inventory(resourceMiner.mine_item, resourceMiner.mine_batch_amount)


__all__ = ["ResourceMinerManager"]
