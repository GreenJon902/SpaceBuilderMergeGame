import AppInfo
from lib.ConfigParsers import JSONParser

userSettings: JSONParser = JSONParser(AppInfo.settings_file)
gameData: JSONParser = JSONParser(AppInfo.game_data_file)
