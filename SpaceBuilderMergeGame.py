import os
import pathlib
import sys
from shutil import copyfile

import AppInfo

if __name__ == "__main__":
    if not os.path.exists(AppInfo.user_data_dir):
        os.makedirs(AppInfo.user_data_dir)

    #if not os.path.exists(AppInfo.settings_file):
    copyfile(AppInfo.default_settings_file, AppInfo.settings_file)

    from staticConfigurables import settings

    os.chdir(pathlib.Path(__file__).parent.absolute())
    os.environ["KIVY_HOME"] = AppInfo.kivy_home_dir
    os.environ["KCFG_KIVY_LOG_NAME"] = AppInfo.log_name
    os.environ["KCFG_KIVY_LOG_DIR"] = AppInfo.log_dir
    os.environ["KCFG_KIVY_LOG_LEVEL"] = settings.get("Debug", "log_level")

    import kivy
    from kivy.logger import Logger
    Logger.info("Base: kivy module fully loaded")

    from lib.betterLogger import redo_logger_formatting
    redo_logger_formatting()
    Logger.info("Base: kivy logger overwritten")


    import resources
    from resources import Resources, setup

    setup()
    Resources.load_all()
    Logger.info("Base: resources setup and loaded")
    sys.exit()


    import graphics
    graphics.setup()
    Logger.info("Base: graphics module setup")

    graphics.load_kv()
    Logger.info("Base: kv_language loaded")

    Logger.info("Base: graphics fully loaded")

    graphics.start()

    Logger.info("Base: App has finished!")
