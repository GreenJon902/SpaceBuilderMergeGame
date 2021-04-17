from kivy.animation import Animation, AnimationTransition
from kivy.properties import NumericProperty
from kivy.uix.screenmanager import Screen

from lib.betterLogger import BetterLogger


class LoadingScreen(Screen, BetterLogger):
    loadingScreenShowAnimationLength = NumericProperty(1)

    loadingScreenShowAnimation = None

    def on_enter(self, *args):
        self.loadingScreenShowAnimation = Animation(opacity=1,
                                                    duration=self.loadingScreenShowAnimationLength,
                                                    transition=AnimationTransition.in_out_cubic)
        self.loadingScreenShowAnimation.start(self.ids["content"])
