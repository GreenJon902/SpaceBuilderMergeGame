from kivy.core.image import Image as CoreImage
from kivy.logger import Logger


class _Textures:
    pass


def load(path, section, option):
    Logger.debug("TextureLoader: Starting to load " + str(path) + " for " + str(section) + " | " + str(option))
    coreImage = CoreImage(path)
    Logger.debug("TextureLoader: Opened image")
    texture = coreImage.texture
    Logger.debug("TextureLoader: Converted to texture")

    if section not in Textures.__dict__:
        Textures.__dict__[section] = _Textures()

    Textures.__dict__[section].__dict__[option] = texture
    Logger.info("TextureLoader: Loaded " + str(path) + " for " + str(section) + " | " + str(option))

    return Textures.__dict__[section].__dict__[option]


Textures = _Textures()
