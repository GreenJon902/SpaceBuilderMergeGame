from kivy.properties import StringProperty
from kivy.uix.label import Label

from lib.betterLogger import BetterLogger
from resources import Lang


class MultiLangLabel(Label, BetterLogger):
    text_id = StringProperty("General.NoTextId")

    def __init__(self, *args, **kwargs):
        super(MultiLangLabel, self).__init__(*args, **kwargs)
        self.on_text_id(self, self.text_id)

    def on_text_id(self, instance, value):
        self.text = Lang.get(value)
        self.log_debug("Switching text of", instance, "to \"", value, "\" which is \"", self.text, " \"")