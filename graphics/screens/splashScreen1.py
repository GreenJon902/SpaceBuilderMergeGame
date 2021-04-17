from kivy.animation import Animation, AnimationTransition
from kivy.clock import Clock
from kivy.properties import NumericProperty
from kivy.uix.screenmanager import Screen

from graphics.spaceBuilderMergeGameScreenManager import get_sm
from lib.betterLogger import BetterLogger


class SplashScreen1(Screen, BetterLogger):
    timeBetweenImageSwitched = NumericProperty(1)
    rocketFlyDuration = NumericProperty(1)
    timeTillNextSplashScreen = NumericProperty(1)

    rocketSwitchClock = None
    rocketFlyAnimation = None
    timeTillNextSplashScreenClock = None

    def on_enter(self, *args):
        self.timeTillNextSplashScreenClock = Clock.schedule_once(
            lambda *_: get_sm().set_screen("SplashScreen2"), self.timeTillNextSplashScreen)
        self.rocketSwitchClock = Clock.schedule_interval(self.switch_rockets, self.timeBetweenImageSwitched)
        self.rocketFlyAnimation = Animation(pos_hint={"x": -1}, duration=self.rocketFlyDuration, transition=self.rocketFlyAnimationTransition)
        self.rocketFlyAnimation.start(self.ids["image_a"])
        self.rocketFlyAnimation.start(self.ids["image_b"])

    def switch_rockets(self, *args):
        self.ids["image_a"].opacity *= -1
        self.ids["image_b"].opacity *= -1

    def on_pre_leave(self, *args):
        self.rocketSwitchClock.cancel()
        """self.rocketFlyAnimation.stop(self.ids["image_a"])
        self.rocketFlyAnimation.stop(self.ids["image_b"])"""

    def rocketFlyAnimationTransition(self, progress):
        p = progress * 2
        if p < 1:
            t = AnimationTransition.out_expo(p) / 2
        else:
            t = AnimationTransition.in_quint(p) / 2


        return t

