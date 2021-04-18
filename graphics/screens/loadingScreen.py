from kivy.animation import Animation, AnimationTransition
from kivy.properties import NumericProperty
from kivy.uix.screenmanager import Screen

from lib.betterLogger import BetterLogger

from resources import ResourceLoader
from resources import load_link_files


class LoadingScreen(Screen, BetterLogger):
    loadingScreenShowAnimationLength: NumericProperty = NumericProperty(1)

    loadingScreenShowAnimation: Animation = None

    def on_enter(self, *args):
        self.loadingScreenShowAnimation = Animation(opacity=1,
                                                    duration=self.loadingScreenShowAnimationLength,
                                                    transition=AnimationTransition.in_out_cubic)
        self.loadingScreenShowAnimation.start(self.ids["content"])

    def prepare_resource_loader(self):
        self.log_info("Resource loader started preparing")
        load_link_files()
        ResourceLoader.get_paths()
        self.log_info("Resource loader finished preparing")

    def on_pre_enter(self, *args):
        self.prepare_resource_loader()
        self.ids["loading_bar"].max = len(ResourceLoader.paths)
