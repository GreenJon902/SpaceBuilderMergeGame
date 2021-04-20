from kivy.uix.floatlayout import FloatLayout



class BaseLayout(FloatLayout):
    def __init__(self, *args, **kwargs):
        FloatLayout.__init__(self, *args, **kwargs)
