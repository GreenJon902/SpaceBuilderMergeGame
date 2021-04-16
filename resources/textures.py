from threading import Thread

from kivy.core.image import Image as CoreImage
from kivy.logger import Logger

from lib.betterLogger import BetterLogger
import resources


class _Textures:
    pass


class TextureHolder(BetterLogger):
    __log_name_suffix__ = "_Not Named Yet"

    coreImage = None
    _texture = None
    changed = False

    def set_core_image(self, coreImage):
        self.coreImage = coreImage
        self.changed = True
        self.log_trace("CoreImage set to", coreImage)

    @property
    def texture(self):
        if self._texture is not None and not self.changed:
            self.log_trace("Returning Texture, not none and not changed")
            return self._texture

        else:
            self.log_trace("Updating Texture | _texture -", self._texture, "| changed -", self.changed)
            self.changed = False
            self._texture = self.coreImage.texture
            self.log_trace("Returning Texture")
            return self._texture


def _load(path, section, option, t):
    resources.current_threaded_tasks.append(t)

    Logger.debug("TextureLoader" + "__" + str(section) + "__" + str(option) + ": Starting to load " + str(path) +
                 " for " + str(section) + " | " + str(option))
    coreImage = CoreImage(path)
    Logger.debug("TextureLoader" + "__" + str(section) + "__" + str(option) + ": Opened image")

    Textures.__dict__[section].__dict__[option].set_core_image(coreImage)
    Logger.info("TextureLoader" + "__" + str(section) + "__" + str(option) + ": Loaded " + str(path) + " for " +
                str(section) + " | " + str(option))

    resources.current_threaded_tasks.remove(t)


def load(path, section, option):
    if section not in Textures.__dict__:
        Textures.__dict__[section] = _Textures()

    Textures.__dict__[section].__dict__[option] = TextureHolder()
    Textures.__dict__[section].__dict__[option].__log_name_suffix__ = "__" + str(section) + "__" + str(option)
    t = Thread(target=_load)
    t._args = (path, section, option, t)
    t.start()

    return Textures.__dict__[section].__dict__[option]


Textures = _Textures()

"""

import time
from threading import Thread

from kivy.core.image import Image as CoreImage, Texture
from kivy.logger import Logger



class _Textures:
    pass


def _load(path, section, option):
    Logger.info("TESTING: " + path + section + option)
    Logger.info("TESTING: " + str(2) + str(Textures.__dict__[section].__dict__[option]))
    Logger.debug("TextureLoader: Starting to load " + str(path) + " for " + str(section) + " | " + str(option))
    Logger.info("TESTING: " + str(3) + str(Textures.__dict__[section].__dict__[option]))
    coreImage = CoreImage(path)
    Logger.info("TESTING: " + str(4) + str(Textures.__dict__[section].__dict__[option]) + str(coreImage))
    Logger.debug("TextureLoader: Opened image")
    Logger.info("TESTING: " + str(5) + str(Textures.__dict__[section].__dict__[option]))
    texture = coreImage.texture
    Logger.info("TESTING: " + str(6) + str(Textures.__dict__[section].__dict__[option]) + str(texture))
    Logger.debug("TextureLoader: Converted to texture")
    Logger.info("TESTING: " + str(7) + str(Textures.__dict__[section].__dict__[option]))

    Textures.__dict__[section].__dict__[option] = texture
    Logger.info("TESTING: " + str(8) + str(Textures.__dict__[section].__dict__[option]))
    Logger.info("TextureLoader: Loaded " + str(path) + " for " + str(section) + " | " + str(option))
    Logger.info("TESTING: " + str(9) + str(Textures.__dict__[section].__dict__[option]))


def load(path, section, option):
    if section not in Textures.__dict__:
        Textures.__dict__[section] = _Textures()

    Textures.__dict__[section].__dict__[option] = None
    Logger.info("TESTING: " + str(1) + str(Textures.__dict__[section].__dict__[option]))
    Thread(target=_load, args=(path, section, option)).start()
    Logger.info("TESTING: " + "end" + str(Textures.__dict__[section].__dict__[option]))
    time.sleep(5)

    return Textures.__dict__[section].__dict__[option]


Textures = _Textures()


"""
