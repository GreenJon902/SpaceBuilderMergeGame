from kivy.properties import BooleanProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image

from graphics import graphicsConfig
from graphics.customWidgets.betterButton import TextBetterButton
from lib import ignore_args
from lib.betterLogger import BetterLogger


class MergeGUI(BetterLogger, FloatLayout):
    active: str = BooleanProperty(None)

    def __init__(self, **kwargs):
        BetterLogger.__init__(self)
        FloatLayout.__init__(self, **kwargs)

        self.size_hint = None, None

    def set_all(self, items: dict):
        self.log_deep_debug("Set all to", items)

        self.clear_widgets()

        for item, amount in items.items():
            b = TextBetterButton(button_id=str(item) + "_item", size_type="big", show_amount_text=True, amount=amount)
            b.bind(on_release=ignore_args(self.item_pressed, b))
            b.button_storage = str(item)
            self.add_widget(b)

            self.log_deep_debug("Added button -", b)

        self._trigger_layout()


    def item_pressed(self, button: TextBetterButton):
        pass


    def on_active(self, _instance, value: bool):
        if bool(value):
            self.opacity = 1

        else:
            self.opacity = 0



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

