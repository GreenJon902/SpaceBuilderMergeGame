from configparser import ConfigParser, ExtendedInterpolation

import AppInfo

# We no need bc of resources
"""class _pathConfigParser(ConfigParser):
    def get(self, *args, **kwargs) -> str:
        path = super(_pathConfigParser, self).get(*args, **kwargs)
        return os.path.join(AppInfo.resources_dir, path)


textures = _pathConfigParser(interpolation=ExtendedInterpolation()) 
textures.read(AppInfo.texture_link_file)

fonts = _pathConfigParser(interpolation=ExtendedInterpolation())
fonts.read(AppInfo.font_link_file)

texts = ConfigParser(interpolation=ExtendedInterpolation())
texts.read(AppInfo.texts_file)"""

settings = ConfigParser(interpolation=ExtendedInterpolation())


graphics = ConfigParser(interpolation=ExtendedInterpolation())


def read():
    global settings, graphics
    settings.read(AppInfo.settings_file)
    graphics.read(AppInfo.graphics_file)
