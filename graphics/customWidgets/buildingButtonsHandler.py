from kivy.uix.boxlayout import BoxLayout

from graphics.customWidgets.betterButton import BetterButton
from lib.betterLogger import BetterLogger


class BuildingButtonsHandler(BoxLayout, BetterLogger):
    def __init__(self, **kwargs):
        BetterLogger.__init__(self)
        BoxLayout.__init__(self, **kwargs)

    def redo_buttons(self, button_ids: list[str]):
        self.clear_widgets()

        button_id: str
        for button_id in button_ids:
            button = BetterButton(button_id=button_id, size_type="big")
            self.add_widget(button)

        self.log_trace("Added buttons to self and deleted old, new are", self.children)
