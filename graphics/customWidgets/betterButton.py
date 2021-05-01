from kivy.input import MotionEvent
from kivy.properties import OptionProperty, StringProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.widget import Widget

from resources import Textures
from configurables import graphicsConfig


class BetterButton(ButtonBehavior, Widget):
    size_type: OptionProperty = OptionProperty(options=["small", "big"], defaultvalue="small")
    button_id: StringProperty = StringProperty(defaultvalue="None")
    mouse_down: bool = False

    def __init__(self, *args, **kwargs):
        ButtonBehavior.__init__(self)
        Widget.__init__(self, *args, **kwargs)


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
            self.ids["fg_image"].texture = Textures.get("Buttons", str(self.button_id))


        self.ids["bg_image"].texture = Textures.get("Buttons", "bg_" + str(self.size_type))

        self.size_hint_y = graphicsConfig.getfloat("Buttons", "size_hint_y_" + str(self.size_type))

    def on_height(self, instance, value: int):
        self.width = value

