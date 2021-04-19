import json
import os
from configparser import ExtendedInterpolation

from AppInfo import resources_dir
from lib.betterLogger import BetterLogger
from lib.ConfigParsers import PathConfigParser

from resources.lang import Lang
from resources.textures import Textures
from resources import textures

from kivy.core.image import Image as CoreImage


current_threaded_tasks = list()


class ResourceLinks(BetterLogger):
    audio: PathConfigParser = PathConfigParser(interpolation=ExtendedInterpolation())
    font: PathConfigParser = PathConfigParser(interpolation=ExtendedInterpolation())
    language: PathConfigParser = PathConfigParser(interpolation=ExtendedInterpolation())
    textures: PathConfigParser = PathConfigParser(interpolation=ExtendedInterpolation())

    audio_file_name: str = "audioLink.ini"
    font_file_name: str = "fontLink.ini"
    language_file_name: str = "langLink.ini"
    textures_file_name: str = "textureLink.ini"

    array: {str: PathConfigParser} = {
        "audio": audio,
        "font": font,
        "language": language,
        "textures": textures}

    def __init__(self, *args, **kwargs):
        super(ResourceLinks, self).__init__(*args, **kwargs)
        self.audio.__log_name_prefix__ = "Audio_"
        self.font.__log_name_prefix__ = "Font_"
        self.language.__log_name_prefix__ = "Language_"
        self.textures.__log_name_prefix__ = "Textures_"

    def load_link_files(self):
        self.log_debug("Loading link files")

        self.audio.read(os.path.join(resources_dir, self.audio_file_name))
        self.font.read(os.path.join(resources_dir, self.font_file_name))
        self.language.read(os.path.join(resources_dir, self.language_file_name))
        self.textures.read(os.path.join(resources_dir, self.textures_file_name))

        self.log_info("Loaded link files")


class ResourceLoader(BetterLogger):
    paths_to_resources: dict[str, any] = {}
    tasks_completed: int = -1
    total_links: int = 0
    tasks: list[dict[str, any]] = list()

    @property
    def number_of_tasks_to_do(self) -> int:
        return self.total_links + len(self.paths_to_resources) + 1  # +1 is order task list

    def get_tasks(self):
        ResourceLinks.load_link_files()
        self.get_paths()

    def get_paths(self):
        self.log_info("Starting to load all paths")

        for link_name in ResourceLinks.array:
            self.__log_name_suffix__ = "_" + str(link_name)
            link: PathConfigParser = ResourceLinks.array[link_name]
            self.log_debug("Loading paths from", link)

            for section in link.sections():
                for option in link.options(section):
                    self.log_trace("Getting path from |", section, "|", option, "...")
                    path: str = link.get(section, option)
                    self.log_trace("Path is", path)

                    self.total_links += 1

                    if path not in self.paths_to_resources:
                        self.paths_to_resources[path] = None
                        self.tasks.append({
                            "type": "load_resource",
                            "resource_type": link_name,
                            "path": path
                        })
                        self.log_trace("Appended to list")
                    else:
                        self.log_trace("Already in list, no changes!")
                    self.tasks.append({
                        "type": "deal_resources",
                        "resource_type": link_name,
                        "section": section,
                        "option": option,
                        "path": path
                    })
                    self.log_trace()

        self.__log_name_suffix__ = ""
        self.log_info("Finished loading all paths")
        self.log_info(self.total_links, "links found")


    # def load_resource_from_path(self, path: str):
    #   time.sleep(1)


    def run_next_task(self) -> bool:
        # self.load_resource_from_path(str(self.paths_to_resources[list(self.paths_to_resources.keys())[self.paths_loaded]]))

        if self.tasks_completed == -1:  # order task list
            self.log_trace("Ordering task list")

            correct_order_of_tasks: list[str] = list(["load_resource", "deal_resources"])
            new_tasks_list: list[dict[str, any]] = list()

            for to_look_for in correct_order_of_tasks:
                for task in self.tasks:
                    if task["type"] == to_look_for:
                        new_tasks_list.append(task)

            self.tasks = new_tasks_list

            self.log_trace("Ordered task list -\n", str(self.tasks).replace("}, {", "},\n {"))

        else:  # Task list is ordered
            self.log_trace("Doing next task. Number is", self.tasks_completed)

            self.run_task(self.tasks[self.tasks_completed])



        self.tasks_completed += 1
        if self.tasks_completed == self.number_of_tasks_to_do - 1:  # is done | -1 bc we need to order
            return True
        else:
            return False

    def run_task(self, task_info):
        self.log_trace("Current task array is", task_info)

        if task_info["type"] == "load_resource":

            if task_info["resource_type"] == "language":
                array = json.load(open(task_info["path"] + ".json", "r"))
                array = lang.convert(array)
                self.paths_to_resources[task_info["path"]] = array

            elif task_info["resource_type"] == "textures":
                core_image = CoreImage.load(task_info["path"])
                self.paths_to_resources[task_info["path"]] = core_image

            elif task_info["resource_type"] == "audio":
                pass

            elif task_info["resource_type"] == "font":
                pass

            else:
                self.log_critical("No know resource_type -", task_info["resource_type"])


        elif task_info["type"] == "deal_resources":
            if task_info["resource_type"] == "language":
                Lang.register_array(self.paths_to_resources[task_info["path"]], task_info["option"])

            elif task_info["resource_type"] == "textures":
                Textures.register(task_info["section"], task_info["option"], self.paths_to_resources[task_info["path"]])

            elif task_info["resource_type"] == "audio":
                pass

            elif task_info["resource_type"] == "font":
                pass

            else:
                self.log_critical("No know resource_type -", task_info["resource_type"])

        else:
            self.log_critical("No know task type -", task_info["name"])

    """loaded = {}

    def load_all(self):
        self.log_info("Starting to load all ResourceFiles")

        for link_name in ResourceLinks.array:
            self.log_debug("-"*100, "Loading from", link_name, "link", "-"*50)
            link = ResourceLinks.array[link_name]
            self.log_debug("Link ConfigParser is", link)

            for section in link.sections():
                for option in link.options(section):
                    self._load(link_name, section, option)

            self.log_debug("-"*100, "Finished loading from", link_name, "-"*50)
            # self.log_debug("\n")
            # self.log_debug("")

        self.log_info("-"*100, "Finished looping through resource files, waiting for threads to finish""-"*100)
        while len(current_threaded_tasks):
            self.log_trace("Threads left -", current_threaded_tasks)
        self.log_info("-"*100, "All threads finished!" + "-"*100)



    def _load(self, resource_type, section, option):
        self.__log_name_suffix__ = "___" + str(resource_type) + "__" + str(section) + "__" + str(option)
        self.log_debug("Loading", resource_type, "with the .ini path", (section, option))

        if resource_type not in self.loaded:
            self.loaded[resource_type] = {}

        if section not in self.loaded[resource_type]:
            self.loaded[resource_type][section] = {}

        if resource_type in self.loaded:
            if section in self.loaded[resource_type]:
                if option in self.loaded[resource_type][section]:
                    self.log_debug("Resource already loaded, skipping")

                else:
                    link = ResourceLinks.array[resource_type]
                    path = link.get(section, option)

                    self.log_debug("Got path -", path)

                    if resource_type == "language":
                        array = json.load(open(path + ".json", "r"))
                        self.log_debug(array)
                        Lang.register_array(array, option)

                        self.loaded[resource_type][section][option] = Lang.get_all(option)

                    if resource_type == "textures":
                        self.loaded[resource_type][section][option] = textures.load(path, section, option)


        # self.log_debug("")
        self.__log_name_suffix__ = """""



ResourceLoader: ResourceLoader = ResourceLoader()
ResourceLinks: ResourceLinks = ResourceLinks()

__all__ = ["ResourceLoader", "Lang", "Textures"]
