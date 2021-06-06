from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from kivy.input import MotionEvent


from kivy.graphics.transformation import Matrix
from kivy.properties import NumericProperty
from kivy.uix.scatterlayout import ScatterLayout

import graphics
from configurables import userSettings
from graphics import graphicsConfig
from lib.betterLogger import BetterLogger


class BetterScatter(ScatterLayout, BetterLogger):
    scale_min: int = NumericProperty(defaultvalue=graphicsConfig.getfloat("BaseBuildScreen", "min_zoom"))  # out
    scale_max: int = NumericProperty(defaultvalue=graphicsConfig.getfloat("BaseBuildScreen", "max_zoom"))  # in
    scroll_sensitivity: int = NumericProperty(defaultvalue=userSettings.getfloat("controls", "scroll_sensitivity"))
    base_layout_on_touch_up_function: callable = None

    def __init__(self, **kwargs):
        ScatterLayout.__init__(self, **kwargs)
        BetterLogger.__init__(self)
        self.register_event_type("on_transformed")

    def on_touch_down(self, touch: MotionEvent):
        if touch.is_mouse_scrolling:
            # dx, dy, dz = 0, 0, 0
            # z = self.scale

            if touch.button == 'scrolldown':

                if self.scale < self.scale_max:

                    nextScale = self.scale * (1 + self.scroll_sensitivity)
                    if nextScale < self.scale_max:
                        self.scale = nextScale

                    else:
                        self.scale = self.scale_max


            elif touch.button == 'scrollup':
                if self.scale > self.scale_min:

                    nextScale = self.scale * (1 - self.scroll_sensitivity)
                    if nextScale > self.scale_min:
                        self.scale = nextScale

                    else:
                        self.scale = self.scale_min

            else:
                self.log_warning("Touch event was sent and mouse was scrolling but not up or down - ", touch)

            # bdz = self.scale - z
            # self.dispatch("on_transformed", dx, dy, dz)
            self.dispatch("on_transform_with_touch", touch)

        else:
            ScatterLayout.on_touch_down(self, touch)

        self.fix_transform_edges(touch)


    def on_touch_move(self, touch: MotionEvent):
        ScatterLayout.on_touch_move(self, touch)
        self.fix_transform_edges(touch)


    def on_touch_up(self, touch: MotionEvent):
        ScatterLayout.on_touch_up(self, touch)
        dx, dy = touch.ox - touch.x, touch.oy - touch.y

        if (graphicsConfig.getint("BaseLayout", "maximum_move_distance_for_select") * -1) <= dx <= \
                graphicsConfig.getint("BaseLayout", "maximum_move_distance_for_select") and \
                (graphicsConfig.getint("BaseLayout", "maximum_move_distance_for_select") * -1) <= dy <= \
                graphicsConfig.getint("BaseLayout", "maximum_move_distance_for_select") and not \
                touch.is_mouse_scrolling and touch.grab_current == self:

            self.log_deep_debug("Touch up and within 5 of touch origin, running base layout building select")
            self.base_layout_on_touch_up_function(*self.to_local(*touch.pos))

        self.fix_transform_edges(touch)

    def fix_transform_edges(self, touch: MotionEvent):
        (left, bottom), (width, height) = self.bbox
        right, top = left + width, bottom + height

        dx, dy, dz = 0, 0, 0

        if left > 0:
            dx = 0 - left

        elif right < graphics.width():
            dx = graphics.width() - right

        if bottom > 0:
            dy = 0 - bottom

        elif top < graphics.height():
            dy = graphics.height() - top



        self.apply_transform(Matrix().translate(dx, dy, dz))
        self.dispatch("on_transform_with_touch", touch)



    def collide_point(self, x: int, y: int):  # from scatter plane because ScatterPlaneLayout it didn't do layout well
        return True

    def on_transformed(self, dx, dy, dz):
        pass

    def reset(self):
        self.scale = 1
        self.rotation = 0
        self.pos = 0, 0


__all__ = ["BetterScatter"]
