import math

from kivy.clock import Clock
from kivy.input import MotionEvent
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget

from graphics.buildings.buildingbase import BuildingBase
from graphics.customWidgets.betterButton import BetterButton
from graphics.customWidgets.betterScatter import BetterScatter
from graphics.spaceBuilderMergeGameScreenManager import get_screen
from lib.betterLogger import BetterLogger


class BuildingButtonsHandler(FloatLayout, BetterLogger):
    spacer1: Widget = Widget()
    spacer2: Widget = Widget()
    custom_buttons_holder: BoxLayout = BoxLayout()
    move_buttons_holder: FloatLayout = FloatLayout()
    scatter: BetterScatter = None

    last_rotation: float = 0

    transform_button_1: BetterButton = None
    transform_button_2: BetterButton = None

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

        if building.movable:  # TODO: Fix problem of buttons going everywhere because of fix of positioning
            self.transform_button_1 = BetterButton(button_id="move", size_type="small",
                                                   on_touch_down=self.button_touch_down,
                                                   on_touch_move=self.button_touch_move,
                                                   on_touch_up=self.button_touch_up,
                                                   button_storage=building)
            self.transform_button_2 = BetterButton(button_id="rotate", size_type="small",
                                                   on_touch_down=self.button_touch_down,
                                                   on_touch_move=self.button_touch_move,
                                                   on_touch_up=self.button_touch_up,
                                                   button_storage=building)
            get_screen("BaseBuildScreen").ids["scatter"].bind(
                on_transform_with_touch=lambda _instance, _value: self.redo_building_move_buttons(building),
                size=lambda _instance, _value: print(_instance, _value))

            self.move_buttons_holder.add_widget(self.transform_button_1)
            self.move_buttons_holder.add_widget(self.transform_button_2)

            # TODO: Find better solution
            Clock.schedule_once(lambda _elapsed_time: self.redo_building_move_buttons(building), 0)


        self.log_deep_debug("Added buttons to self, they are", self.custom_buttons_holder.children)

    def redo_building_move_buttons(self, building):
        (x, y), (x2, y2) = building.get_projected_corners()
        x, y = self.scatter.to_parent(x, y)
        x2, y2 = self.scatter.to_parent(x2, y2)

        self.transform_button_1.right, self.transform_button_1.top = x, y
        self.transform_button_2.x, self.transform_button_2.y = x2, y2

    def clear_buttons(self):
        get_screen("BaseBuildScreen").ids["scatter"].unbind(on_transform_with_touch=self.redo_building_move_buttons,
                                                            size=self.redo_building_move_buttons)

        self.move_buttons_holder.clear_widgets()
        self.custom_buttons_holder.clear_widgets()
        self.log_deep_debug("Cleared buttons")

    def button_touch_down(self, button: BetterButton, touch: MotionEvent):
        if not touch.is_mouse_scrolling and button.collide_point(touch.x, touch.y):
            self.log_deep_debug("Started transforming building with button", button)
            touch.grab(button)

            building: BuildingBase = button.button_storage

            building_x, building_y = self.scatter.to_parent(*building.get_projected_origin())

            mouse_x = touch.x
            mouse_y = touch.y

            mouse_dx = mouse_x - building_x  # adjacent
            mouse_dy = mouse_y - building_y  # opposite

            try:
                self.last_rotation = math.degrees(math.atan(mouse_dy / mouse_dx))

            except ZeroDivisionError:
                self.last_rotation = math.degrees(math.atan(mouse_dy / mouse_dx + 1))


    def button_touch_move(self, button: BetterButton, touch: MotionEvent):
        if touch.grab_current == button:
            building: BuildingBase = button.button_storage

            if button.button_id == "move":  # TODO: Make this a bit better
                building.x += touch.dx / (15 * self.scatter.scale)
                building.y += touch.dy / (15 * self.scatter.scale)


            elif button.button_id == "rotate":
                building_x, building_y = self.scatter.to_parent(*building.get_projected_origin())

                mouse_x = touch.x
                mouse_y = touch.y

                mouse_dx = mouse_x - building_x  # adjacent
                mouse_dy = mouse_y - building_y  # opposite

                try:
                    rot = math.degrees(math.atan2(mouse_dy, mouse_dx))
                    delta_rot = rot - self.last_rotation
                    building.rotation += delta_rot
                    self.last_rotation = rot

                except ZeroDivisionError:
                    self.log_warning("Got ZeroDivisionError from rotating building | mouse_dx, mouse_dy =",
                                     mouse_dx, mouse_dy)



            else:
                self.log_critical("Wrong button type for building transform buttons -", button.button_id)

            self.redo_building_move_buttons(building)

    def button_touch_up(self, button: BetterButton, touch: MotionEvent):
        if touch.grab_current == button:
            self.log_deep_debug("Finished transforming building with button", button)  # TODO: Remove double logging
            touch.ungrab(button)


building_button_id_to_function: dict[str, callable] = {
    "store": lambda building: building.store(),
    "scrap": lambda building: building.scrap()
}


def button_pressed(better_button: BetterButton):
    try:
        function = building_button_id_to_function[better_button.button_id]

    except KeyError:
        better_button.log_warning("Couldn't find function in building_button_id_to_function with the type -",
                                  better_button.button_id)
        return

    function(better_button.button_storage)


__all__ = ["BuildingButtonsHandler"]
