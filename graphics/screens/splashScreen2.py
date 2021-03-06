from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    # noinspection PyProtectedMember
    from kivy._clock import ClockEvent
    from kivy.animation import Animation


from kivy.animation import Animation, AnimationTransition
from kivy.clock import Clock
from kivy.properties import NumericProperty
from kivy.uix.screenmanager import Screen

from graphics.preLoadScreenManager import get_sm
from lib.betterLogger import BetterLogger


class SplashScreen2(Screen, BetterLogger):
    waitBeforeTitleStartShow: int = NumericProperty(1)
    titleShowAnimationLength: int = NumericProperty(1)
    titleShowLength: int = NumericProperty(1)
    titleFadeAnimationLength: int = NumericProperty(1)
    timeTillLoadingScreen: int = NumericProperty(4)

    timeTillLoadingScreenClock: ClockEvent = None
    animation: Animation = None

    def on_enter(self, *args: any):
        self.timeTillLoadingScreenClock = Clock.schedule_once(
            lambda *_: get_sm().set_screen("LoadingScreen"), self.timeTillLoadingScreen)
        self.animation = Animation(opacity=0,
                                       duration=self.waitBeforeTitleStartShow,
                                       transition=AnimationTransition.linear) + \
                             Animation(opacity=1,
                                       duration=self.titleShowAnimationLength,
                                       transition=AnimationTransition.in_sine) + \
                             Animation(opacity=1,
                                       duration=self.titleShowLength,
                                       transition=AnimationTransition.linear) + \
                             Animation(opacity=0,
                                       duration=self.titleFadeAnimationLength,
                                       transition=AnimationTransition.out_expo)
        self.animation.start(self.ids["image_a"])


    def on_pre_leave(self, *args: any):
        self.animation.stop(self.ids["image_a"])


__all__ = ["SplashScreen2"]
