from kivy.properties import OptionProperty, StringProperty, NumericProperty, ObjectProperty, BooleanProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.uix.widget import Widget

from graphics import graphicsConfig
from lib.betterLogger import BetterLogger
from resources import Textures


class BetterButton(ButtonBehavior, Widget, BetterLogger):
    button_storage: any = ObjectProperty(None)
    size_type: str = OptionProperty("small", options=["small", "big", "flat"])
    bg_type: str = OptionProperty("both_blues", options=["dark_blue", "both_blues", "light_blue"])
    button_id: str = StringProperty("None")
    mouse_down: bool = False
    force_size_hint_y: int = NumericProperty(None)
    let_parent_size: bool = BooleanProperty(False)

    bg_image: Image = None
    fg_image: Image = None

    def __init__(self, **kwargs):
        self.bg_image = Image(allow_stretch=True, keep_ratio=True)
        self.fg_image = Image(allow_stretch=True, keep_ratio=True)
        self.size_hint = None, None

        BetterLogger.__init__(self)

        ButtonBehavior.__init__(self)
        Widget.__init__(self, **kwargs)

        self.add_widget(self.bg_image)
        self.add_widget(self.fg_image)


    def on_force_size_hint_y(self, _instance, value):
        if value is not None:
            self.size_hint_y = value


    def on_kv_post(self, base_widget: Widget):
        self.update()

    def on_size_type(self, _instance, _value: str):
        self.update()

    def on_button_id(self, _instance, _value: str):
        self.update()


    def update(self):
        if self.button_id == "None":
            self.fg_image.opacity = 0
        else:
            self.fg_image.opacity = 1
            try:
                self.fg_image.texture = Textures.get("Buttons", str(self.button_id))
            except KeyError:
                self.fg_image.opacity = 0
                self.log_critical("No know texture -", "Buttons -", str(self.button_id))

        self.bg_image.pos = self.pos
        self.bg_image.size = self.size
        self.fg_image.pos = self.pos
        self.fg_image.size = self.size

        self.bg_image.texture = Textures.get("Buttons", "bg_" + str(self.bg_type))

        if not self.let_parent_size:
            if self.force_size_hint_y is None:
                self.size_hint_y = graphicsConfig.getfloat("Buttons", "size_hint_y_" + str(self.size_type))

    def on_height(self, _, value: int):
        if not self.let_parent_size:
            self.width = value


    def on_pos(self, _, pos):
        self.bg_image.pos = pos
        self.fg_image.pos = pos

    def on_size(self, _, size):
        self.bg_image.size = size
        self.fg_image.size = size

    def __repr__(self):
        return "BetterButton(button_id=" + str(self.button_id) + ", size_type=" + str(self.size_type) + ", bg_type=" + \
               str(self.bg_type) + ", button_storage=" + str(self.button_storage) + ")"
