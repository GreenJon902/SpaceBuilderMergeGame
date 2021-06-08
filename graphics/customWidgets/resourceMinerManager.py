from __future__ import annotations

from typing import TYPE_CHECKING

from configurables import gameData
from graphics.customWidgets.betterScatter import BetterScatter
from graphics.spaceBuilderMergeGameScreenManager import get_screen

if TYPE_CHECKING:
    from graphics.buildings import ResourceMiner
    from kivy.input import MotionEvent

from kivy.properties import StringProperty
from kivy.uix.image import Image

from resources import Textures
from kivy.uix.floatlayout import FloatLayout

from lib.betterLogger import BetterLogger
from lib.globalEvents import GlobalEvents


class ResourceMinerManager(FloatLayout, BetterLogger):
    resource_miner_finished_icons: dict[int, ResourceMinerFinishedIcon] = {}

    def __init__(self, **kwargs):
        BetterLogger.__init__(self)
        FloatLayout.__init__(self, **kwargs)

        GlobalEvents.bind(mine_batch_finished=self.batch_finished)
        GlobalEvents.bind(remove_mine_finished_icon=self.remove_finished_icon)
        GlobalEvents.bind(on_scatter_transformed=self.update_positions)

    def batch_finished(self, resourceMiner: ResourceMiner):
        if resourceMiner.id not in self.resource_miner_finished_icons:
            (x1, y1), (x2, y2) = resourceMiner.get_projected_corners()
            x = x1 + ((x2 - x1) / 2)
            y = y2

            finished_icon = ClickableResourceMinerFinishedIcon(pos=(x, y), resource_name=resourceMiner.mine_item)
            finished_icon.resource_miner_id = resourceMiner.id
            self.resource_miner_finished_icons[resourceMiner.id] = finished_icon
            self.add_widget(finished_icon)


        self.resource_miner_finished_icons[resourceMiner.id].amount_that_has_been_mined += \
            resourceMiner.mine_batch_amount

    def remove_finished_icon(self, icon: ResourceMinerFinishedIcon):
        self.remove_widget(icon)
        del self.resource_miner_finished_icons[icon.resource_miner_id]


    def update_positions(self):  # TODO: Do something building is moved
        scatter: BetterScatter = get_screen("BaseBuildScreen").ids["scatter"]

        for building_id, icon in self.resource_miner_finished_icons.items():
            building = get_screen("BaseBuildScreen").ids["base_layout"].buildings[int(building_id)]
            (x1, y1), (x2, y2) = building.get_projected_corners()
            x = x1 + ((x2 - x1) / 2)
            y = y2

            icon.pos = scatter.to_parent(x, y)


class ResourceMinerFinishedIcon(FloatLayout, BetterLogger):
    amount_that_has_been_mined: int = 0

    bg_image: Image = None
    fg_image: Image = None

    resource_name: str = StringProperty("None")
    resource_miner_id: int = None

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


class ClickableResourceMinerFinishedIcon(ResourceMinerFinishedIcon):
    def on_touch_down(self, touch: MotionEvent):
        if self.collide_point(*touch.pos):
            gameData.add_to_inventory(self.resource_name, self.amount_that_has_been_mined)
            GlobalEvents.dispatch("remove_mine_finished_icon", self)
            self.log_deep_debug("Clicked on, added", self.amount_that_has_been_mined, "of", self.resource_name,
                                "to the inventory")


__all__ = ["ResourceMinerManager"]
