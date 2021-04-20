from kivy.graphics.transformation import Matrix
from kivy.input import MotionEvent
from kivy.properties import NumericProperty
from kivy.uix.scatterlayout import ScatterLayout

import graphics
import staticConfigurables
from lib.betterLogger import BetterLogger


class BetterScatter(ScatterLayout, BetterLogger):
    scale_min: NumericProperty = staticConfigurables.graphics.getfloat("BaseBuildScreen", "min_zoom")  # out
    scale_max: NumericProperty = staticConfigurables.graphics.getfloat("BaseBuildScreen", "max_zoom")  # in
    scroll_sensitivity: NumericProperty = staticConfigurables.settings.getfloat("Controls", "scroll_sensitivity")

    def __init__(self, *args, **kwargs):
        ScatterLayout.__init__(self, *args, **kwargs)
        BetterLogger.__init__(self)

    def on_touch_down(self, touch: MotionEvent):
        if touch.is_mouse_scrolling:

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
                self.log_warning("Touch event was sent and mouse was scrolling but not up nor down - ", touch)

            self.dispatch("on_transform_with_touch", touch)

        else:
            ScatterLayout.on_touch_down(self, touch)

    def on_transform_with_touch(self, touch: MotionEvent):
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


    def collide_point(self, x: int, y: int):  # from scatter plane because ScatterPlaneLayout it didn't do layout well
        return True


    def reset(self):
        self.scale = 1
        self.rotation = 0
        self.pos = 0, 0
