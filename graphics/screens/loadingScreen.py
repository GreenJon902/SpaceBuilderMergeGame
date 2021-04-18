from kivy._clock import ClockEvent
from kivy.animation import Animation, AnimationTransition
from kivy.clock import Clock
from kivy.properties import NumericProperty
from kivy.uix.screenmanager import Screen

from lib.betterLogger import BetterLogger
import time

from resources import ResourceLoader
from resources import load_link_files


class LoadingScreen(Screen, BetterLogger):
    loadingScreenShowAnimationLength: NumericProperty = NumericProperty(1)

    loadingScreenShowAnimation: Animation = None
    loadNextResourceClock: ClockEvent = None

    def on_enter(self, *args: any):
        self.loadingScreenShowAnimation = Animation(opacity=1,
                                                    duration=self.loadingScreenShowAnimationLength,
                                                    transition=AnimationTransition.in_out_cubic)
        self.loadingScreenShowAnimation.bind(on_complete=lambda *_: self.start_next_task_clock())
        self.loadingScreenShowAnimation.start(self.ids["content"])


    def start_next_task_clock(self):
        self.loadNextResourceClock = Clock.schedule_interval(lambda *_: self.run_next_task(), 0)

    def prepare_resource_loader(self):
        self.log_info("Resource loader started preparing")
        load_link_files()
        ResourceLoader.get_paths()
        self.log_info("Resource loader finished preparing")

    def on_pre_enter(self, *args):
        self.prepare_resource_loader()
        self.ids["loading_bar"].max = ResourceLoader.number_of_tasks_to_do

    def run_next_task(self):
        t: int = time.time()
        is_done = ResourceLoader.run_next_task()

        if is_done:
            self.log_info("Finished all tasks -", ResourceLoader.paths_to_resources)
            self.loadNextResourceClock.cancel()

        self.ids["loading_bar"].value += 1
        self.log_debug("Finished task", int(self.ids["loading_bar"].value), "out of",
                       ResourceLoader.number_of_tasks_to_do, "in", time.time() - t)
