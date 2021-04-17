from kivy.animation import Animation, AnimationTransition
from kivy.clock import Clock
from kivy.properties import NumericProperty
from kivy.uix.screenmanager import Screen

from graphics.spaceBuilderMergeGameScreenManager import get_sm
from lib.betterLogger import BetterLogger


class SplashScreen2(Screen, BetterLogger):
    waitBeforeTitleStartShow = NumericProperty(1)
    titleShowAnimationLength = NumericProperty(1)
    titleShowLength = NumericProperty(1)
    titleFadeAnimationLength = NumericProperty(1)
    timeTillLoadingScreen = NumericProperty(4)

    timeTillLoadingScreenClock = None
    animation = None

    def on_enter(self, *args):
        self.timeTillLoadingScreenClock = Clock.schedule_once(
            lambda *_: get_sm().set_screen("LoadingScreen"), self.timeTillLoadingScreen)
        self.animation = Animation(opacity=0,
                                       duration=self.waitBeforeTitleStartShow,
                                       transition=AnimationTransition.linear) + \
                             Animation(opacity=1,
                                       duration=self.titleShowAnimationLength,
                                       transition=AnimationTransition.out_sine) + \
                             Animation(opacity=1,
                                       duration=self.titleShowLength,
                                       transition=AnimationTransition.linear) + \
                             Animation(opacity=0,
                                       duration=self.titleFadeAnimationLength,
                                       transition=AnimationTransition.out_expo)
        self.animation.start(self.ids["image_a"])


    def on_pre_leave(self, *args):
        self.animation.stop(self.ids["image_a"])
