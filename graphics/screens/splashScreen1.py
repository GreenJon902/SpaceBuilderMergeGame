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


def rocketFlyAnimationTransition(progress: float) -> float:
    p: float = progress * 2
    if p < 1:
        t: float = AnimationTransition.out_expo(p) / 2
    else:
        t: float = AnimationTransition.in_quint(p) / 2

    return t


class SplashScreen1(Screen, BetterLogger):
    timeBetweenImageSwitched: NumericProperty = NumericProperty(1)
    rocketFlyDuration: NumericProperty = NumericProperty(1)
    timeTillNextSplashScreen: NumericProperty = NumericProperty(1)

    rocketSwitchClock: ClockEvent = None
    rocketFlyAnimation: Animation = None
    timeTillNextSplashScreenClock: ClockEvent = None

    def on_enter(self, *args: any):
        self.timeTillNextSplashScreenClock = Clock.schedule_once(
            lambda *_: get_sm().set_screen("SplashScreen2"), self.timeTillNextSplashScreen)
        self.rocketSwitchClock = Clock.schedule_interval(self.switch_rockets, self.timeBetweenImageSwitched)
        self.rocketFlyAnimation = Animation(pos_hint={"x": -1}, duration=self.rocketFlyDuration,
                                            transition=rocketFlyAnimationTransition)
        self.rocketFlyAnimation.start(self.ids["image_a"])
        self.rocketFlyAnimation.start(self.ids["image_b"])

    def switch_rockets(self, _elapsed_time):
        self.ids["image_a"].opacity *= -1
        self.ids["image_b"].opacity *= -1

    def on_pre_leave(self, *args: any):
        self.rocketSwitchClock.cancel()
        """self.rocketFlyAnimation.stop(self.ids["image_a"])
        self.rocketFlyAnimation.stop(self.ids["image_b"])"""


__all__ = ["SplashScreen1"]
