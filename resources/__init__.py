import json
import os
from configparser import ExtendedInterpolation

from AppInfo import resources_dir
from lib.betterLogger import BetterLogger
from lib.pathConfigParser import PathConfigParser

from resources.lang import Lang
from resources.textures import Textures
from resources import textures


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

    def load_link_files(self):
        self.log_debug("Loading link files")

        self.audio.read(os.path.join(resources_dir, self.audio_file_name))
        self.font.read(os.path.join(resources_dir, self.font_file_name))
        self.language.read(os.path.join(resources_dir, self.language_file_name))
        self.textures.read(os.path.join(resources_dir, self.textures_file_name))

        self.log_info("Loaded link files")


class ResourceLoader(BetterLogger):
    paths: [str] = list()

    def load_paths(self):
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

                    if path not in self.paths:
                        self.paths.append(path)
                        self.log_trace("Appended to list")
                    else:
                        self.log_trace("Already in list, no changes!")
                    self.log_trace()

        self.__log_name_suffix__ = ""
        self.log_info("Finished loading all paths")
        self.log_info("Paths are -", self.paths)

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


def load_link_files():
    ResourceLinks.load_link_files()


ResourceLoader: ResourceLoader = ResourceLoader()
ResourceLinks: ResourceLinks = ResourceLinks()

__all__ = ["ResourceLoader", "Lang", "Textures", "load_link_files"]
