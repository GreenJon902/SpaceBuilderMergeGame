from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget

from graphics.customWidgets.betterButton import BetterButton
from graphics.customWidgets.betterScatter import BetterScatter
from graphics.customWidgets.buildings.buildingbase import BuildingBase
from graphics.spaceBuilderMergeGameScreenManager import get_screen
from lib.betterLogger import BetterLogger


class BuildingButtonsHandler(FloatLayout, BetterLogger):
    spacer1: Widget = Widget()
    spacer2: Widget = Widget()
    custom_buttons_holder: BoxLayout = BoxLayout()
    move_buttons_holder: FloatLayout = FloatLayout()
    scatter: BetterScatter = None

    def __init__(self, **kwargs):
        BetterLogger.__init__(self)
        FloatLayout.__init__(self, **kwargs)

        self.add_widget(self.move_buttons_holder)
        self.add_widget(self.custom_buttons_holder)


    def on_size(self, _instance, _size):
        self.custom_buttons_holder.size = _size
        self.move_buttons_holder.size = _size


    def redo_buttons(self, button_ids: list[str], building: BuildingBase):
        self.scatter = get_screen("BaseBuildScreen").ids["scatter"]
        # Hacky fix so its not got every time the scatter is transformed

        self.clear_buttons()

        self.custom_buttons_holder.add_widget(self.spacer1)

        button_id: str
        for button_id in button_ids:
            button = BetterButton(button_id=button_id, size_type="big", on_release=button_pressed,
                                  button_storage=building)
            self.custom_buttons_holder.add_widget(button)

        self.custom_buttons_holder.add_widget(self.spacer2)

        (x, y), (x2, y2) = building.get_corners()
        x, y = get_screen("BaseBuildScreen").ids["scatter"].to_parent(x, y)
        x2, y2 = get_screen("BaseBuildScreen").ids["scatter"].to_parent(x2, y2)

        b1 = BetterButton(button_id="move", size_type="small", pos=(x, y), on_touch_down=self.move_button_touch_down)
        b2 = BetterButton(button_id="move", size_type="small", pos=(x2, y2), on_touch_down=self.move_button_touch_down)
        get_screen("BaseBuildScreen").ids["scatter"].bind(
            on_transform_with_touch=lambda _instance, _value: self.redo_building_move_buttons(building, b1, b2))

        self.move_buttons_holder.add_widget(b1)
        self.move_buttons_holder.add_widget(b2)


        self.log_trace("Added buttons to self, they are", self.custom_buttons_holder.children)


    def redo_building_move_buttons(self, building, b1, b2):
        (x, y), (x2, y2) = building.get_corners()
        x, y = self.scatter.to_parent(x, y)
        x2, y2 = self.scatter.to_parent(x2, y2)

        b1.x, b1.y = x, y
        b2.x, b2.y = x2, y2


    def clear_buttons(self):
        get_screen("BaseBuildScreen").ids["scatter"].unbind(on_transform_with_touch=self.redo_building_move_buttons)

        self.move_buttons_holder.clear_widgets()
        self.custom_buttons_holder.clear_widgets()
        self.log_trace("Cleared buttons")


    def move_button_touch_down(self, button, touch): # TODO: Implement this
        if button.collide_point(touch.x, touch.y):
            print(1)
        else:
            print(2)


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
