from kivy.properties import OptionProperty, StringProperty, NumericProperty, ObjectProperty, BooleanProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.widget import Widget

from graphics import graphicsConfig
from lib.betterLogger import BetterLogger
from resources import Textures


class BetterButton(ButtonBehavior, FloatLayout, BetterLogger):  # TODO: Fix bug where functions are ran too many times
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

        BetterLogger.__init__(self)
        ButtonBehavior.__init__(self)
        Widget.__init__(self, **kwargs)

        self.add_widget(self.bg_image)
        self.add_widget(self.fg_image)

        self.bg_image.texture = Textures.get("Buttons", "bg_" + str(self.bg_type))
        self.size_hint_x = None
        self.size_hint_y = graphicsConfig.getfloat("Buttons", "size_hint_y_" + str(self.size_type))



    def on_bg_type(self, _instance, bg_type):
        self.bg_image.texture = Textures.get("Buttons", "bg_" + str(bg_type))


    def update_size_hint(self):
        if not self.let_parent_size:
            if self.force_size_hint_y is None:
                self.size_hint_y = graphicsConfig.getfloat("Buttons", "size_hint_y_" + str(self.size_type))
                self.size_hint_x = None

            else:
                self.size_hint_y = None
                self.size_hint_x = None

        else:
            self.size_hint_y = 1
            self.size_hint_x = None

    def on_let_parent_size(self, _instance, _value):
        self.update_size_hint()

    def on_force_size_hint_y(self, _instance, _value):
        self.update_size_hint()


    def on_size_type(self, _instance, _value: str):
        self.update_size_hint()

    def on_button_id(self, _instance, _value: str):
        if self.button_id == "None":
            self.fg_image.opacity = 0
        else:
            self.fg_image.opacity = 1
            try:
                self.fg_image.texture = Textures.get("Buttons", str(self.button_id))
            except KeyError:
                self.fg_image.opacity = 0
                self.log_critical("No know texture -", "Buttons -", str(self.button_id))


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

    def __repr__(self):
        return "BetterButton(button_id=" + str(self.button_id) + ", size_type=" + str(self.size_type) + ", bg_type=" + \
               str(self.bg_type) + ", button_storage=" + str(self.button_storage) + ")"



class TextBetterButton(BetterButton):
    show_main_text: bool = BooleanProperty(False)
    show_amount_text: bool = BooleanProperty(False)
    amount: int = NumericProperty(0)

    main_text: Label = None
    amount_text: Label = None

    def __init__(self, **kwargs):
        self.main_text = Label(halign=graphicsConfig.get("Buttons", "amount_text_valign"),
                               valign=graphicsConfig.get("Buttons", "amount_text_halign"),
                               font_name="Buttons-amount_text")
        self.amount_text = Label(halign=graphicsConfig.get("Buttons", "amount_text_valign"),
                                 valign=graphicsConfig.get("Buttons", "amount_text_halign"),
                                 font_name="Buttons-amount_text")

        BetterButton.__init__(self, **kwargs)

        self.add_widget(self.main_text)
        self.add_widget(self.amount_text)


    def on_pos(self, _instance, pos: tuple[int, int]):
        BetterButton.on_pos(self, _instance, pos)

        self.amount_text.right = pos[0] + (self.width * 0.9)
        self.amount_text.y = pos[1] + (self.height * 0)

    def on_size(self, _instance, size: tuple[int, int]):
        BetterButton.on_pos(self, _instance, size)

        self.amount_text.size = size
        self.amount_text.text_size = size

        """self.amount_text.center_x = self.x + (size[0] * 0.9)
        self.amount_text.center_y = self.y + (size[1] * 0.1)"""



    def on_amount(self, _instance, value: int):
        self.amount_text.text = "x" + str(value)


    def __repr__(self):
        return "TextBetterButton(button_id=" + str(self.button_id) + ", size_type=" + str(self.size_type) + \
               ", bg_type=" + str(self.bg_type) + ", button_storage=" + str(self.button_storage) + ", show_main_text=" \
               + str(self.show_main_text) + ", show_amount_text=" + str(self.show_amount_text) + ", amount=" + \
               str(self.amount) + ")"
