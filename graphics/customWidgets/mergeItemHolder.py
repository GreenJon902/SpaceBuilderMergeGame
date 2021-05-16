from kivy.properties import ObjectProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image


class MergeItemHolder(FloatLayout):

    bg_image: Image = ObjectProperty()
