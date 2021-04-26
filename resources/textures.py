from kivy.core.image import Image as CoreImage

from lib.betterLogger import BetterLogger


class EmptyClass:
    pass


class Textures(BetterLogger):
    __log_name__ = "Textures"

    def register(self, section: str, option: str, core_image: CoreImage):
        self.log_trace("Registering texture", core_image, "for", section, option)

        if not hasattr(self, section):
            setattr(self, section, EmptyClass())

        setattr(getattr(self, section), option, core_image)



Textures: Textures = Textures()
