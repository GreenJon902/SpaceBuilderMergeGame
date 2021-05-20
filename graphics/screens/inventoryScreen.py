from kivy.properties import ColorProperty
from kivy.uix.screenmanager import Screen

from configurables import gameData
from graphics import graphicsConfig, height
from graphics.customWidgets.betterButton import TextBetterButton, FlatBetterButton
from graphics.customWidgets.mergeGUI import MergeGUI
from lib import ignore_args
from lib.betterLogger import BetterLogger
from resources import GameConfig


class InventoryScreen(Screen, BetterLogger):
    merge_layout_cover_color = ColorProperty([0, 0, 0, 0])

    merge_option: str = None

    current_merge_output_button_id = "unknown_item"
    current_recipe_button_id = "unknown_item"


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
            b = TextBetterButton(button_id=str(item) + "_item", size_type="big", show_amount_text=True, amount=amount)
            b.bind(on_release=ignore_args(self.item_pressed, b))
            b.button_storage = str(item)
            self.ids["inventory_items_holder"].add_widget(b)

            self.log_deep_debug("Added button -", b)


    def item_pressed(self, button: TextBetterButton):
        if self.merge_option == "place":
            building_type = str(button.button_storage)

            if building_type in GameConfig.get("Buildings", "list"):
                gameData.move_to_placed_buildings(building_type)

                self.update_inventory()

            else:
                self.log_deep_debug("Item", building_type, "was clicked on but is not a building")

        elif self.merge_option == "recipes":
            item = str(button.button_storage)

            if item in GameConfig.get("Items", "recipes"):
                recipe = GameConfig.get("Items", "recipes", item)
                self.log_deep_debug("Creating GUI for recipe of item", item, "| Recipe is", recipe)

                self.ids["recipe_gui"].set_all(recipe)
                self.current_recipe_button_id = item + "_item"
                self.ids["merge_output_button"].button_id = item + "_item"

            else:
                self.log_deep_debug("Item", item, "was clicked on but is doesnt have a merge recipe")

        elif self.merge_option == "merge":
            item = str(button.button_storage)

            if self.ids["merge_gui"].get_moved_amount(item) < gameData.get("inventory")[item]:
                self.ids["merge_gui"].add(item)

            else:
                self.log_deep_debug("Item was pressed while merge mode active cant move anymore because all "
                                    "have already been moved")

            self.update_merge_option_gui_output()

        else:
            self.log_critical("No know merge option", self.merge_option)


    def update_merge_option_gui_output(self):
        items = list(self.ids["merge_gui"].get_all())
        self.log_deep_debug("Updating merge option gui output with items -", items)


        has_changed_image = False


        for recipe_product, recipe in GameConfig.get("Items", "recipes").items():
            correct = True
            print(1, recipe, items, len(items), len(recipe), len(items) == len(recipe))

            if len(items) == len(recipe):  # If not then it cant be, this is probably more efficient
                print(2, recipe, items, len(items), len(recipe), len(items) == len(recipe))
                for i1 in recipe.items():
                    for i2 in items:
                        matched = False

                        if i1[0] == i2[0]:
                            if i1[1] <= i2[1]:
                                self.log_deep_debug("Correct match for merge recipe part", i1, i2)
                                matched = True

                        if not matched:
                            self.log_deep_debug("No merge recipe part", i1, i2)

                            correct = False


            if correct:
                self.log_deep_debug("All merge recipe part matches found, item is", recipe_product)
                self.ids["merge_output_button"].button_id = str(recipe_product) + "_item"
                has_changed_image = True
                break

        if not has_changed_image:
            self.ids["merge_output_button"].button_id = "unknown_item"



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
        outer_color = graphicsConfig.getdict("Buttons", "flat_color")
        label_color = graphicsConfig.getdict("Buttons", "flat_label_color")

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


        merge_gui: MergeGUI = self.ids["merge_gui"]
        recipe_gui: MergeGUI = self.ids["recipe_gui"]
        handled = False

        if id_of_clicked == "merge_option_place":
            handled = True


            self.merge_layout_cover_color = graphicsConfig.getdict("InventoryScreen", "merge_cover_active_color")
            self.merge_option = "place"

            merge_gui.active = False
            recipe_gui.active = False

            self.ids["merge_output_button"].button_id = "unknown_item"

        else:
            self.merge_layout_cover_color = 0, 0, 0, 0

        if id_of_clicked == "merge_option_recipes":
            handled = True
            self.log_deep_debug("Switched merge option to recipes")

            self.merge_option = "recipes"

            merge_gui.active = False
            recipe_gui.active = True

            self.ids["merge_output_button"].button_id = self.current_recipe_button_id

        if id_of_clicked == "merge_option_merge":
            handled = True
            self.log_deep_debug("Switched merge option to merge")

            self.merge_option = "merge"

            merge_gui.active = True
            recipe_gui.active = False

            self.ids["merge_output_button"].button_id = self.current_merge_output_button_id

        if not handled:
            self.log_critical("No know merge option", id_of_clicked)
