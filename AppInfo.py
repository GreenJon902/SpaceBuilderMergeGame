import os
import appdirs

appname: str = "SpaceBuilderMergeGame"
appauthor: str = "GreenJon902"
version: str = "ALPHA_V0.0.4"
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
default_files_dir: str = os.path.join(resources_dir, "DefaultFiles")
default_settings_file: str = os.path.join(default_files_dir, "defaultSettings.json")
default_game_data_file: str = os.path.join(default_files_dir, "defaultGameData.json")
default_user_data: str = os.path.join(default_files_dir, "defaultUserData.ini")
settings_file: str = os.path.join(user_data_dir, "settings.json")
game_data_file: str = os.path.join(user_data_dir, "gameData.json")
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
loading_screen_background_image: str = os.path.join(pre_load_dir, "loading_screen_background.png")
loading_screen_title_image: str = os.path.join(pre_load_dir, "loading_screen_title.png")
loading_screen_loading_text_font: str = os.path.join(pre_load_dir, "loading_screen_loading_text_font.otf")

default_size: [int] = 700, 500

__all__ = ["appname", "appauthor", "version", "roaming",
           "array",
           "user_data_dir", "kivy_home_dir", "config_dir", "code_dir", "default_settings_file", "settings_file",
           "log_dir", "resources_dir", "kv_language_dir", "graphics_file", "default_user_data",
           "default_size", "log_name", "log_class_length", "default_game_data_file", "game_data_file",
           "pre_load_dir", "pre_load_kv_lang_path", "splash_screen_images", "loading_screen_background_image",
           "loading_screen_title_image", "loading_screen_loading_text_font"]
