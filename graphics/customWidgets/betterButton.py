from kivy.properties import OptionProperty, StringProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.widget import Widget

from graphics import graphicsConfig
from lib.betterLogger import BetterLogger
from resources import Textures


class BetterButton(ButtonBehavior, Widget, BetterLogger):
    size_type: OptionProperty = OptionProperty(options=["small", "big"], defaultvalue="small")
    button_id: StringProperty = StringProperty(defaultvalue="None")
    mouse_down: bool = False

    def __init__(self, *args, **kwargs):
        BetterLogger.__init__(self)
        ButtonBehavior.__init__(self)
        Widget.__init__(self, *args, **kwargs)

        self.size_hint = None, None


    def on_kv_post(self, base_widget):
        self.update()

    def on_size_type(self, *args):
        self.update()

    def on_button_id(self, *args):
        self.update()

    def update(self):
        if self.button_id == "None":
            self.ids["fg_image"].opacity = 0
        else:
            self.ids["fg_image"].opacity = 1
            try:
                self.ids["fg_image"].texture = Textures.get("Buttons", str(self.button_id))
            except KeyError:
                self.ids["fg_image"].opacity = 0
                self.log_critical("No know texture -", "Buttons", str(self.button_id))


        self.ids["bg_image"].texture = Textures.get("Buttons", "bg_" + str(self.size_type))

        self.size_hint_y = graphicsConfig.getfloat("Buttons", "size_hint_y_" + str(self.size_type))

    def on_height(self, instance, value: int):
        self.width = value

