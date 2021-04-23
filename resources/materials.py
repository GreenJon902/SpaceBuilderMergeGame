from kivy.core.image import Image as CoreImage

from lib.betterLogger import BetterLogger
from resources.textures import EmptyClass


class Materials(BetterLogger):
    __log_name__ = "Materials"

    def register_mtl(self, mtl_str):
        self.log_trace("Registering mtl file")

    def register(self, section: str, option: str, core_image: CoreImage):
        self.log_trace("Registering material", core_image, "for", section, option)

        if section not in self.__dict__:
            self.__dict__[section] = EmptyClass()

        self.__dict__[section].__dict__[option] = core_image


Materials: Materials = Materials()
