from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget

from graphics.customWidgets.betterButton import BetterButton
from graphics.customWidgets.buildings.buildingbase import BuildingBase
from lib.betterLogger import BetterLogger


class BuildingButtonsHandler(FloatLayout, BetterLogger):
    spacer1: Widget = Widget()
    spacer2: Widget = Widget()
    custom_buttons_holder: BoxLayout = BoxLayout()
    move_buttons_holder: FloatLayout = FloatLayout()

    def __init__(self, **kwargs):
        BetterLogger.__init__(self)
        FloatLayout.__init__(self, **kwargs)

        self.add_widget(self.move_buttons_holder)
        self.add_widget(self.custom_buttons_holder)

    def get_positions_of_move_buttons(self, building: BuildingBase) -> tuple[tuple[int, int], tuple[int, int]]:
        print(building.get_corners())

    def redo_buttons(self, button_ids: list[str], building: BuildingBase):
        self.clear_buttons()

        self.custom_buttons_holder.add_widget(self.spacer1)

        button_id: str
        for button_id in button_ids:
            button = BetterButton(button_id=button_id, size_type="big", on_release=button_pressed,
                                  button_storage=building)
            self.custom_buttons_holder.add_widget(button)

        self.custom_buttons_holder.add_widget(self.spacer2)


        self.get_positions_of_move_buttons(building)

        self.log_trace("Added buttons to self, they are", self.custom_buttons_holder.children)


    def clear_buttons(self):
        self.custom_buttons_holder.clear_widgets()
        self.log_trace("Cleared buttons")


building_button_id_to_function: dict[str, callable] = {
    "store": lambda building: building.store()
}


def button_pressed(better_button: BetterButton):
    try:
        function = building_button_id_to_function[better_button.button_id]

    except KeyError:
        better_button.log_warning("Couldn't find function in building_button_id_to_function with the id -",
                                  better_button.button_id)
        return

    function(better_button.button_storage)
