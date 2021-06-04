import AppInfo
from lib.ConfigParsers import JSONParser, GameDataJSONParser

userSettings: JSONParser = JSONParser(AppInfo.settings_file)
gameData: GameDataJSONParser = GameDataJSONParser(AppInfo.game_data_file)


__all__ = ["userSettings", "gameData"]
