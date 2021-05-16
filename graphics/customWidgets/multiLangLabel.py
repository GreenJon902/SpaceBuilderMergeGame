from kivy.core.image import Texture
from kivy.core.text import DEFAULT_FONT
from kivy.properties import StringProperty, ColorProperty
from kivy.uix.image import Image
from kivy.uix.label import Label

from lib.betterLogger import BetterLogger
from resources import Lang


class MultiLangLabel(Image, BetterLogger):
    text_id: str = StringProperty("General.NoTextId")
    font_name: str = StringProperty(DEFAULT_FONT)
    color: dict = ColorProperty([1, 1, 1, 1])
    _text: str = ""

    _label: Label = Label(font_size="1000dp")

    def __init__(self, **kwargs: any):
        BetterLogger.__init__(self)
        Image.__init__(self, **kwargs)
        self.on_text_id(self, self.text_id)

    def on_text_id(self, instance, value: str):
        self._text: str = Lang.get(value)
        self.log_debug("Switching text of", instance, "to \"", value, "\" which is \"", self._text, " \"")
        self.do_texture()

    def on_font_name(self, _instance, _value):
        self.do_texture()

    def on_size(self, _instance, _value):
        self.do_texture()

    def do_texture(self):
        self._label.text = self._text
        self._label.font_name = self.font_name
        self._label.color = self.color

        self._label.texture_update()
        self.texture = self._label.texture
        self.texture: Texture
        try:
            self.texture.bind()
            # TODO: Find a better way that doesnt slow down the window but still makes the texture not go black
        except AttributeError:
            pass
        # self.source = "./ResourceFiles/Textures/buttons/chests.png"

    def on_color(self, _instance, value):
        self.do_texture()
