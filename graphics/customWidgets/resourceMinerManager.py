from __future__ import annotations

from typing import TYPE_CHECKING

from kivy.properties import StringProperty
from kivy.uix.image import Image

from resources import Textures

if TYPE_CHECKING:
    from graphics.buildings import ResourceMiner


from kivy.uix.floatlayout import FloatLayout

from lib.betterLogger import BetterLogger
from lib.globalEvents import GlobalEvents


class ResourceMinerManager(FloatLayout, BetterLogger):
    resource_miner_finished_icons: dict[int, ResourceMinerFinishedIcon] = {}

    def __init__(self, **kwargs):
        BetterLogger.__init__(self)
        FloatLayout.__init__(self, **kwargs)

        GlobalEvents.bind(mine_batch_finished=self.batch_finished)

    # noinspection PyMethodMayBeStatic
    # ignore because we will do something else with this later
    def batch_finished(self, resourceMiner: ResourceMiner):
        # gameData.add_to_inventory(resourceMiner.mine_item, resourceMiner.mine_batch_amount)

        if resourceMiner.id not in self.resource_miner_finished_icons:
            (x1, y1), (x2, y2) = resourceMiner.get_projected_corners()
            x = x1 + ((x2 - x1) / 2)
            y = y2

            finished_icon = ResourceMinerFinishedIcon(pos=(x, y), resource_name=resourceMiner.mine_item)
            self.resource_miner_finished_icons[resourceMiner.id] = finished_icon
            self.add_widget(finished_icon)


        self.resource_miner_finished_icons[resourceMiner.id].amount_that_has_been_mined += \
            resourceMiner.mine_batch_amount


class ResourceMinerFinishedIcon(FloatLayout, BetterLogger):
    amount_that_has_been_mined: int = 0

    bg_image: Image = None
    fg_image: Image = None

    resource_name: str = StringProperty("None")

    def __init__(self, **kwargs):
        self.bg_image = Image(allow_stretch=True, keep_ratio=True)
        self.fg_image = Image(allow_stretch=True, keep_ratio=True)

        BetterLogger.__init__(self)
        FloatLayout.__init__(self, **kwargs)

        self.bg_image.texture = Textures.get("ResourceMiner", "finished_icon_bg")

        self.size_hint_x = None
        self.size_hint_y = 0.1

        self.add_widget(self.bg_image)
        self.add_widget(self.fg_image)


    def on_resource_name(self, _instance, _value: str):
        if self.resource_name == "None":
            self.fg_image.opacity = 0
        else:
            self.fg_image.opacity = 1
            try:
                self.fg_image.texture = Textures.get("ResourceMiner", str(self.resource_name))
            except KeyError:
                self.fg_image.opacity = 0
                self.log_critical("No know texture -", "ResourceMiner -", str(self.resource_name))


    def on_height(self, _instance, height: int):
        self.width = height

        self.bg_image.width = height
        self.fg_image.width = height

    def on_pos(self, _instance, pos):
        self.bg_image.pos = pos
        self.fg_image.pos = pos

    def on_width(self, _instance, width):
        self.bg_image.width = width
        self.fg_image.width = width


__all__ = ["ResourceMinerManager"]
