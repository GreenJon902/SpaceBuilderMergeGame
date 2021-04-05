import os
import pathlib
from shutil import copyfile

import AppInfo

if __name__ == "__main__":
    if not os.path.exists(AppInfo.user_data_dir):
        os.makedirs(AppInfo.user_data_dir)

    if not os.path.exists(AppInfo.settings_file):
        copyfile(AppInfo.default_settings_file, AppInfo.settings_file)

    from staticConfigurables import settings

    os.chdir(pathlib.Path(__file__).parent.absolute())
    os.environ["KIVY_HOME"] = AppInfo.kivy_home_dir
    os.environ["KCFG_KIVY_LOG_NAME"] = settings.get("Debug", "log_name")
    os.environ["KCFG_KIVY_LOG_DIR"] = AppInfo.log_dir
    os.environ["KCFG_KIVY_LOG_LEVEL"] = settings.get("Debug", "log_level")

    import kivy
    from kivy.logger import Logger

    from kivy.logger import Logger
    import misc.loggerWithTime

    Logger.info("Base: kivy module fully loaded")

    import Graphics

    Graphics.setup()
    Logger.info("Base: Graphics setup")

    Graphics.load_kv()
    Logger.info("Base: kv_language loaded")

    Logger.info("Base: Graphics fully loaded")

    Graphics.start()

    Logger.info("Base: App has finished!")
