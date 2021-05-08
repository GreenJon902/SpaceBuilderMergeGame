from kivy.factory import Factory
from kivy.uix.boxlayout import BoxLayout


class ScreenManagerSwitcher(BoxLayout):
    current = None

    def __init__(self, **kwargs):
        BoxLayout.__init__(self, **kwargs)

        self.manager1 = Factory.PreLoadScreenManager
        self.manager2 = Factory.SpaceBuilderMergeGameScreenManager

        m = self.manager1()
        self.current = m
        self.add_widget(m)


    def switch(self):
        self.remove_widget(self.children[0])
        m = self.manager2()
        self.current = m
        self.add_widget(m)
