from configparser import ExtendedInterpolation

import AppInfo
from lib.ConfigParsers import ExtendedConfigParser

graphicsConfig: ExtendedConfigParser = ExtendedConfigParser(interpolation=ExtendedInterpolation())
ExtendedConfigParser.__log_name_prefix__ = "Graphics_"
graphicsConfig.read(AppInfo.graphics_file)
