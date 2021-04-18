from configparser import ConfigParser, ExtendedInterpolation

import AppInfo

Settings: ConfigParser = ConfigParser(interpolation=ExtendedInterpolation())
Settings.read(AppInfo.settings_file)
