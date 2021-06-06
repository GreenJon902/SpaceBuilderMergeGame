from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass


from kivy.animation import Animation
from kivy.uix.screenmanager import Screen

from graphics import graphicsConfig
from lib.betterLogger import BetterLogger


class BaseBuildScreen(Screen, BetterLogger):
    def fade_in(self):
        self.opacity = 0
        a = Animation(opacity=1, duration=graphicsConfig.getfloat("General", "transition_length"))
        a.start(self)
        # TODO: Make fade in not look like poop after toilet


__all__ = ["BaseBuildScreen"]
