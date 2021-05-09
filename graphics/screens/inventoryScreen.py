from kivy.uix.screenmanager import Screen

from configurables import gameData
from graphics import graphicsConfig, height
from graphics.customWidgets.betterButton import BetterButton
from lib.betterLogger import BetterLogger


class InventoryScreen(Screen, BetterLogger):
    def __init__(self, **kwargs):
        BetterLogger.__init__(self)
        Screen.__init__(self, **kwargs)

    def on_pre_enter(self, *args):
        self.ids["inventory_items_holder"].bind(size=self.on_inventory_items_holder_size)

        self.ids["inventory_items_holder"].clear_widgets()

        unordered_items: dict[str, int] = dict(gameData.get("inventory"))
        # TODO: order items
        items = unordered_items

        for item, amount in items.items():
            b = BetterButton(button_id=str(item), size_type="big")
            self.ids["inventory_items_holder"].add_widget(b)

            self.log_trace("Added button -", b)

    def on_touch_down(self, touch):
        Screen.on_touch_down(self, touch)

    def on_inventory_items_holder_size(self, _instance, _size):
        holder_width = self.ids["inventory_items_holder"].width

        button_size = height() * graphicsConfig.getfloat("Buttons", "size_hint_y_big")

        buildings_per_row = int(holder_width / button_size)
        extra_space = holder_width - (buildings_per_row * button_size)

        for building in self.ids["inventory_items_holder"].children:
            building.width = (height() * graphicsConfig.getfloat("Buttons", "size_hint_y_big")) + \
                             (extra_space / buildings_per_row)
            building.height = height() * graphicsConfig.getfloat("Buttons", "size_hint_y_big")

            # TODO: fix bug where not proper sizing on first open
