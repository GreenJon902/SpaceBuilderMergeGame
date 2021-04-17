import os
import appdirs

appname: str = "SpaceBuilderMergeGame"
appauthor: str = "GreenJon902"
version: str = "ALPHA_V0.0.2"
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
pre_load_dir: str = os.path.join(resources_dir, "PreLoadResources")
pre_load_kv_lang_path: str = os.path.join(pre_load_dir, "pre_load_kv_lang.kv")
splash_screen_images: [str] = os.path.join(pre_load_dir, "splash_screen_1_a.png"), \
                              os.path.join(pre_load_dir, "splash_screen_1_b.png"), \
                              os.path.join(pre_load_dir, "splash_screen_2_a.png")

default_size: [int] = 700, 500

__all__ = ["appname", "appauthor", "version", "roaming",
           "array",
           "user_data_dir", "kivy_home_dir", "config_dir", "code_dir", "default_settings_file", "settings_file",
           "log_dir", "resources_dir", "kv_language_dir", "graphics_file",
           "default_size", "log_name", "log_class_length",
           "pre_load_dir", "pre_load_kv_lang_path", "splash_screen_images"]
