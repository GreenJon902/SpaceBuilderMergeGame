import os
from configparser import ConfigParser, ExtendedInterpolation

import AppInfo


class _pathConfigParser(ConfigParser):
    def get(self, *args, **kwargs) -> str:
        path = super(_pathConfigParser, self).get(*args, **kwargs)
        return os.path.join(AppInfo.resources_dir, path)


textures = _pathConfigParser(interpolation=ExtendedInterpolation())
textures.read(AppInfo.texture_link_file)

fonts = _pathConfigParser(interpolation=ExtendedInterpolation())
fonts.read(AppInfo.font_link_file)

texts = ConfigParser(interpolation=ExtendedInterpolation())
texts.read(AppInfo.texts_file)

settings = ConfigParser(interpolation=ExtendedInterpolation())
settings.read(AppInfo.settings_file)

graphics = ConfigParser(interpolation=ExtendedInterpolation())
graphics.read(AppInfo.graphics_file)
