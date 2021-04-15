import json
import os
from configparser import ExtendedInterpolation

from AppInfo import resources_dir
from lib.betterLogger import BetterLogger
from lib.pathConfigParser import PathConfigParser
from resources.lang import Lang


class ResourceLinks(BetterLogger):
    audio = PathConfigParser(interpolation=ExtendedInterpolation())
    font = PathConfigParser(interpolation=ExtendedInterpolation())
    language = PathConfigParser(interpolation=ExtendedInterpolation())
    textures = PathConfigParser(interpolation=ExtendedInterpolation())

    audio_file_name = "audioLink.ini"
    font_file_name = "fontLink.ini"
    language_file_name = "langLink.ini"
    textures_file_name = "textureLink.ini"

    array = {
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


class Resources(BetterLogger):
    loaded = {}

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
            self.log_debug("\n")
            self.log_debug("")



    def _load(self, resource_type, section, option):
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


        self.log_debug("")


def setup():
    ResourceLinks.load_link_files()


Resources = Resources()
ResourceLinks = ResourceLinks()
