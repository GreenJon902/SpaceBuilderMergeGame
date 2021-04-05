import os
import appdirs

appname: str = "[AppName]"
appauthor: str = "[Author]"
version: str = "[Version]"
roaming: bool = False

array: {str: any} = {"appname": appname,
                     "appauthor": appauthor,
                     "version": version,
                     "roaming": roaming}

AppDirs: appdirs.AppDirs = appdirs.AppDirs(**array)

user_data_dir: str = AppDirs.user_data_dir
kivy_home_dir: str = os.path.join(user_data_dir, "kivy")
config_dir: str = os.path.join(user_data_dir, "config")
code_dir: str = os.path.dirname(os.path.realpath(__file__))
default_settings_file: str = os.path.join(code_dir, "Resources/default_settings.ini")
settings_file: str = os.path.join(user_data_dir, "settings.json")
resources_dir: str = os.path.join(code_dir, "Resources")
texture_link_file: str = os.path.join(resources_dir, "textureLink.ini")
font_link_file: str = os.path.join(resources_dir, "fontLink.ini")
graphics_file: str = os.path.join(resources_dir, "graphicsConfig.ini")
texts_file: str = os.path.join(resources_dir, "texts.ini")
kv_language_dir: str = os.path.join(resources_dir, "kv_language")
log_dir: str = AppDirs.user_log_dir

default_size: [int] = 700, 500

__all__ = ["appname", "appauthor", "version", "roaming",
           "array",
           "user_data_dir", "kivy_home_dir", "config_dir", "code_dir", "default_settings_file", "settings_file",
           "log_dir", "resources_dir", "texture_link_file", "kv_language_dir", "graphics_file", "font_link_file",
           "default_size", "texts_file"]
