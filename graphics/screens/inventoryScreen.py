import functools

from kivy.properties import ColorProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen

from configurables import gameData
from graphics import graphicsConfig, height
from graphics.customWidgets.betterButton import TextBetterButton, FlatBetterButton
from lib.betterLogger import BetterLogger


# From https://stackoverflow.com/a/32922362/11411477 bc i dont know stuff like this well
def ignore_args(func, *args, **kwargs):
    @functools.wraps(func)
    def newfunc(*_args, **_kwargs):
        return func(*args, **kwargs)
    return newfunc



class InventoryScreen(Screen, BetterLogger):
    merge_layout_cover_color = ColorProperty([0, 0, 0, 0])

    merge_option: str = None


    def __init__(self, **kwargs):
        BetterLogger.__init__(self)
        Screen.__init__(self, **kwargs)

    def on_pre_enter(self, *args):
        self.ids["inventory_items_holder"].bind(size=self.on_inventory_items_holder_size)
        self.update_inventory()

        self.merge_option_button_clicked(graphicsConfig.get("InventoryScreen", "default_merge_option_id"))


    def update_inventory(self):
        self.ids["inventory_items_holder"].clear_widgets()

        unordered_items: dict[str, int] = dict(gameData.get("inventory"))
        # TODO: order items
        items = unordered_items

        for item, amount in items.items():
            b = TextBetterButton(button_id=str(item), size_type="big", show_amount_text=True, amount=amount)
            b.bind(on_release=ignore_args(self.item_pressed, b))
            b.button_storage = str(item)
            self.ids["inventory_items_holder"].add_widget(b)

            self.log_trace("Added button -", b)


    def item_pressed(self, button: TextBetterButton):  # TODO: Check if building is actually a building
        if self.merge_option == "place":
            building_type = str(button.button_storage)
            gameData.move_to_placed_buildings(building_type)

            self.update_inventory()


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


    def merge_option_button_clicked(self, id_of_clicked: str):
        outer_color = graphicsConfig.gettuple("Buttons", "flat_color")
        label_color = graphicsConfig.gettuple("Buttons", "flat_label_color")

        button: FlatBetterButton
        for button_id in self.ids:
            if button_id != "merge_option_buttons_holder" and str(button_id).startswith("merge_option_"):
                button = self.ids[button_id]

                if button_id == id_of_clicked:  # TODO: Fix selected text coloring, for some reason its the wrong blue
                    button.bg_color = label_color
                    button.label_color = outer_color

                else:
                    button.bg_color = outer_color
                    button.label_color = label_color


        merge_layout: BoxLayout = self.ids["merge_layout"]
        handled = False

        if id_of_clicked == "merge_option_place":
            handled = True
            self.log_trace("Switched merge option to place")

            self.merge_layout_cover_color = graphicsConfig.gettuple("InventoryScreen", "merge_cover_active_color")
            self.merge_option = "place"

        else:
            self.merge_layout_cover_color = 0, 0, 0, 0

        if not handled:
            self.log_critical("No know merge option", id_of_clicked)
