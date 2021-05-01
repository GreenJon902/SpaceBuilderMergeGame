from configparser import ConfigParser, ExtendedInterpolation

import AppInfo

from lib.ConfigParsers import ExtendedConfigParser

# We no need bc of resources
"""class _pathConfigParser(ConfigParser):
    def get(self, *args, **kwargs) -> str:
        path = ConfigParser.get(self, *args, **kwargs)
        return os.path.join(AppInfo.resources_dir, path)


textures = _pathConfigParser(interpolation=ExtendedInterpolation()) 
textures.read(AppInfo.texture_link_file)

fonts = _pathConfigParser(interpolation=ExtendedInterpolation())
fonts.read(AppInfo.font_link_file)

texts = ConfigParser(interpolation=ExtendedInterpolation())
texts.read(AppInfo.texts_file)"""

settings: ExtendedConfigParser = ExtendedConfigParser(interpolation=ExtendedInterpolation())
ExtendedConfigParser.__log_name_prefix__ = "Settings_"

graphicsConfig: ExtendedConfigParser = ExtendedConfigParser(interpolation=ExtendedInterpolation())
ExtendedConfigParser.__log_name_prefix__ = "Graphics_"

settings.read(AppInfo.settings_file)
graphicsConfig.read(AppInfo.graphics_file)
