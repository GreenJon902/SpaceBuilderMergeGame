from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget

from graphics.customWidgets.betterButton import BetterButton
from lib.betterLogger import BetterLogger


class BuildingButtonsHandler(BoxLayout, BetterLogger):
    spacer1 = Widget()
    spacer2 = Widget()

    def __init__(self, **kwargs):
        BetterLogger.__init__(self)
        BoxLayout.__init__(self, **kwargs)

    def redo_buttons(self, button_ids: list[str]):
        self.clear_buttons()

        self.add_widget(self.spacer1)

        button_id: str
        for button_id in button_ids:
            button = BetterButton(button_id=button_id, size_type="big", on_release=button_pressed)
            self.add_widget(button)

        self.add_widget(self.spacer2)

        self.log_trace("Added buttons to self, they are", self.children)

    def clear_buttons(self):
        self.clear_widgets()
        self.log_trace("Cleared buttons")


building_button_id_to_function: dict[str, callable] = {
    "store": lambda: print("Storing Object")
}


def button_pressed(better_button: BetterButton):
    try:
        function = building_button_id_to_function[better_button.button_id]

    except KeyError:
        better_button.log_warning("Couldn't find function in building_button_id_to_function with the id -",
                                  better_button.button_id)
        return

    function()
