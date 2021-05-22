from kivy.properties import BooleanProperty, OptionProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image

from graphics import graphicsConfig
from graphics.customWidgets.betterButton import TextBetterButton
from lib import ignore_args
from lib.betterLogger import BetterLogger


class MergeGUI(BetterLogger, FloatLayout):
    active: str = BooleanProperty(None)
    mode: str = OptionProperty(None, options=["merge", "recipes"])

    def __init__(self, **kwargs):
        BetterLogger.__init__(self)
        FloatLayout.__init__(self, **kwargs)

        self.size_hint = None, None

        self.register_event_type("on_items")

    def on_items(self, *args):
        pass

    def set_all(self, items: dict):
        self.log_deep_debug("Set all to", items)

        self.clear_widgets()

        for item, amount in items.items():
            button = TextBetterButton(button_id=str(item) + "_item", size_type="big", show_amount_text=True, amount=amount,
                                      bg_visible=False)
            button.bind(on_release=ignore_args(self.item_pressed, button))
            button.button_storage = str(item)
            self.add_widget(button)

            self.log_debug("Added button -", button)

        self._trigger_layout()


    def add(self, item: str):
        button: TextBetterButton
        for button in self.children:
            if button.button_storage == str(item):
                button.amount += 1

                self.dispatch("on_items")
                return

        button = TextBetterButton(button_id=str(item) + "_item", size_type="big", show_amount_text=True, amount=1,
                                  bg_visible=False)
        button.bind(on_release=ignore_args(self.item_pressed, button))
        button.button_storage = str(item)
        self.add_widget(button)

        self.log_debug("Added button -", button)

        self.dispatch("on_items")

    def remove(self, item: str):
        button: TextBetterButton
        for button in self.children:
            if button.button_storage == str(item):
                button.amount -= 1
                if button.amount <= 0:
                    self.remove_widget(button)
                    self.log_debug("Removed", button)

                break

        self.dispatch("on_items")

    def get_moved_amount(self, item: str):
        button: TextBetterButton
        for button in self.children:
            if button.button_storage == str(item):
                return button.amount

        self.log_deep_debug("Ran get_moved_amount but no button had that item - this is probably not a bug")
        return 0

    def get_all(self):
        button: TextBetterButton
        for button in self.children:
            yield button.button_storage, button.amount

    def item_pressed(self, button: TextBetterButton):
        if self.mode == "merge":  # Move back
            self.remove(button.button_storage)


    def on_active(self, _instance, value: bool):
        if bool(value):
            self.opacity = 1

        else:
            self.opacity = 0

        self.log_deep_debug("self.active set to", value, "and self.opacity set to", self.opacity, "for", self)



    def do_layout(self, *args, **kwargs):
        w, h = self.size
        x, y = kwargs.get('pos', self.pos)

        pos_hints: dict[int, float] = graphicsConfig.getdict("InventoryScreen", "merge_gui_pos_hints")

        c: TextBetterButton
        for i, c in enumerate(self.children):
            # size
            shw, shh = c.size_hint
            shw_min, shh_min = c.size_hint_min
            shw_max, shh_max = c.size_hint_max

            if shw is not None and shh is not None:  # Stolen from actual FloatLayout
                c_w = shw * w
                c_h = shh * h

                if shw_min is not None and c_w < shw_min:
                    c_w = shw_min
                elif shw_max is not None and c_w > shw_max:
                    c_w = shw_max

                if shh_min is not None and c_h < shh_min:
                    c_h = shh_min
                elif shh_max is not None and c_h > shh_max:
                    c_h = shh_max
                c.size = c_w, c_h
            elif shw is not None:
                c_w = shw * w

                if shw_min is not None and c_w < shw_min:
                    c_w = shw_min
                elif shw_max is not None and c_w > shw_max:
                    c_w = shw_max
                c.width = c_w
            elif shh is not None:
                c_h = shh * h

                if shh_min is not None and c_h < shh_min:
                    c_h = shh_min
                elif shh_max is not None and c_h > shh_max:
                    c_h = shh_max
                c.height = c_h


            # Pos
            pos_hint = pos_hints[i]
            c.center_x = x + (w * pos_hint[0])
            c.center_y = y + (h * pos_hint[1])



    def do_size(self, instance: Image, _value):
        self.x = instance.center_x - instance.norm_image_size[0] / 2.
        self.y = instance.center_y - instance.norm_image_size[1] / 2.
        self.size = instance.get_norm_image_size()

