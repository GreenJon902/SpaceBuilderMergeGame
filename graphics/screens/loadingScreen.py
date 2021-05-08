import time

# noinspection PyProtectedMember
from kivy._clock import ClockEvent
from kivy.animation import Animation, AnimationTransition
from kivy.app import App
from kivy.clock import Clock
from kivy.properties import NumericProperty
from kivy.uix.screenmanager import Screen

from graphics.spaceBuilderMergeGameScreenManager import get_sm
from lib.betterLogger import BetterLogger
from resources import ResourceLoader


class LoadingScreen(Screen, BetterLogger):
    loadingScreenShowAnimationLength: NumericProperty = NumericProperty(1)

    loadingScreenShowAnimation: Animation = None
    loadNextResourceClock: ClockEvent = None

    startLoadTime: float = 0

    def on_enter(self, *args: any):
        self.loadingScreenShowAnimation = Animation(opacity=1,
                                                    duration=self.loadingScreenShowAnimationLength,
                                                    transition=AnimationTransition.in_out_cubic)
        self.loadingScreenShowAnimation.bind(on_complete=lambda *_: self.start_next_task_clock())
        self.loadingScreenShowAnimation.start(self.ids["content"])


    def start_next_task_clock(self):
        self.startLoadTime = time.time()
        self.loadNextResourceClock = Clock.schedule_interval(lambda *_: self.run_next_task(), 0)

    def prepare_resource_loader(self):
        self.log_info("Resource loader started preparing")
        ResourceLoader.get_tasks()
        self.log_info("Resource loader finished preparing")

    def on_pre_enter(self, *args):
        self.prepare_resource_loader()
        self.ids["loading_bar"].max = ResourceLoader.number_of_tasks_to_do

    def run_next_task(self):
        t: float = time.time()
        is_done = ResourceLoader.run_next_task()


        self.ids["loading_bar"].value += 1
        self.log_debug("Finished task", int(self.ids["loading_bar"].value), "out of",
                       ResourceLoader.number_of_tasks_to_do, "in", time.time() - t)


        if is_done:
            self.log_info("Finished all tasks in", time.time() - self.startLoadTime)
            self.loadNextResourceClock.cancel()

            self.loadingScreenShowAnimation = Animation(opacity=0,
                                                        duration=self.loadingScreenShowAnimationLength,
                                                        transition=AnimationTransition.in_out_cubic)
            self.loadingScreenShowAnimation.bind(on_complete=lambda *_: self.exit())
            self.loadingScreenShowAnimation.start(self.ids["content"])

    def exit(self):
        self.log_debug("Reloading screen manager")
        App.get_running_app().root.switch()
        get_sm().set_screen("BaseBuildScreen")
