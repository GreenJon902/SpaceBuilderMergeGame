import os
import pathlib
from shutil import copyfile

import AppInfo

if __name__ == "__main__":
    if not os.path.exists(AppInfo.user_data_dir):
        os.makedirs(AppInfo.user_data_dir)

    #  if not os.path.exists(AppInfo.settings_file):
    copyfile(AppInfo.default_settings_file, AppInfo.settings_file)
    print("[INFO   ] [BeforeKivy  ] Can't find settings file, copied a new one")

    if not os.path.exists(AppInfo.game_data_file):
        copyfile(AppInfo.default_game_data_file, AppInfo.game_data_file)
        print("[INFO   ] [BeforeKivy  ] Can't find game data file, copied a new one")


    os.chdir(pathlib.Path(__file__).parent.absolute())
    os.environ["KIVY_HOME"] = AppInfo.kivy_home_dir
    os.environ["KCFG_KIVY_LOG_NAME"] = AppInfo.log_name
    os.environ["KCFG_KIVY_LOG_DIR"] = AppInfo.log_dir

    # noinspection PyUnresolvedReferences
    import kivy
    # noinspection PyUnresolvedReferences
    import kivy3
    # noinspection PyUnresolvedReferences
    import kivy.core.window
    # Fixes sigsegv error when loading images because openGL was not initiated-https://github.com/kivy/kivy/issues/6173
    from kivy.logger import Logger
    Logger.info("Base: kivy module fully loaded")

    from lib.betterLogger import redo_logger_formatting, BetterLogger
    redo_logger_formatting()
    Logger.info("Base: kivy logger overwritten")
    base_logger: BetterLogger = BetterLogger(name="Base")

    """
    from resources import Resources, setup

    setup()
    Resources.load_all()
    Logger.info("Base: resources setup and loaded")"""


    import graphics
    graphics.setup()
    base_logger.log_info("graphics module setup")

    graphics.load_pre_load_kv()
    base_logger.log_info("pre load kv_language loaded")

    base_logger.log_info("graphics ready too start")

    graphics.start()

    base_logger.log_info("App has finished!")
