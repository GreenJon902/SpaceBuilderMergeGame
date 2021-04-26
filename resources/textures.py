import enum

from kivy.core.image import Image as CoreImage

from lib.betterLogger import BetterLogger


class EmptyClass:
    pass


class Textures(BetterLogger):
    __log_name__ = "Textures"
    _textures: dict[str, dict[str, CoreImage]] = {}

    def register(self, section: str, option: str, core_image: CoreImage):
        self.log_trace("Registering texture", core_image, "for", section, option)

        if section not in self._textures:
            self._textures[section] = {}

        self._textures[section][option] = core_image

    def get(self, section: str, option: str):
        return self._textures[section][option].texture

    def __getitem__(self, item):
        return self._textures[item]



Textures: Textures = Textures()
