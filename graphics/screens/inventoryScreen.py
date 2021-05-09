from kivy.uix.screenmanager import Screen

from configurables import gameData
from graphics.customWidgets.betterButton import BetterButton
from lib.betterLogger import BetterLogger


class InventoryScreen(Screen, BetterLogger):
    def __init__(self, **kwargs):
        BetterLogger.__init__(self)
        Screen.__init__(self, **kwargs)

    def on_pre_enter(self, *args):
        self.ids["inventory_items_holder"].clear_widgets()

        unordered_items: dict[str, int] = dict(gameData.get("inventory"))
        # TODO: order items
        items = unordered_items

        for item, amount in items.items():
            b = BetterButton(button_id=str(item), let_parent_size=True)
            self.ids["inventory_items_holder"].add_widget(b)

            self.log_trace("Added button -", b)
