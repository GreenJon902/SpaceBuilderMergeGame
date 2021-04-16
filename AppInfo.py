import os
import appdirs

appname: str = "SpaceBuilderMergeGame"
appauthor: str = "GreenJon902"
version: str = "ALPHA_V0.0.1"
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
resources_dir: str = os.path.join(code_dir, "ResourceFiles")
default_settings_file: str = os.path.join(code_dir, resources_dir, "default_settings.ini")
settings_file: str = os.path.join(user_data_dir, "settings.json")
graphics_file: str = os.path.join(resources_dir, "graphicsConfig.ini")
kv_language_dir: str = os.path.join(resources_dir, "kv_language")
log_dir: str = AppDirs.user_log_dir
log_name: str = appname + "_%y-%m-%d_%_.log"
log_class_length: int = 48

default_size: [int] = 700, 500

__all__ = ["appname", "appauthor", "version", "roaming",
           "array",
           "user_data_dir", "kivy_home_dir", "config_dir", "code_dir", "default_settings_file", "settings_file",
           "log_dir", "resources_dir", "kv_language_dir", "graphics_file",
           "default_size", "log_name", "log_class_length"]
