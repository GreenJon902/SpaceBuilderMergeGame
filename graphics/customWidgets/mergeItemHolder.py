from kivy.properties import NumericProperty
from kivy.uix.floatlayout import FloatLayout


class MergeItemHolder(FloatLayout):

    bg_image_width: int = NumericProperty(0)
    bg_image_height: int = NumericProperty(0)
