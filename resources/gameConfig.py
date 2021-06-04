from lib.ConfigParsers import JSONParser
from lib.betterLogger import BetterLogger


class EmptyClass:
    pass


class GameConfig(JSONParser):
    __log_name__ = "GameConfig"

    def __init__(self):
        BetterLogger.__init__(self)

    def register(self, section: str, option: str, parser: JSONParser):
        self.log_deep_debug("Registering config", parser, "for", section, option)

        if section not in self.array:
            self.array[section] = {}

        self.array[section][option] = parser.array

    def save(self):
        self.log_critical("YOU CANNOT SAVE GAME CONFIG, WHAT ARE YOU ON")

    def delete(self, *_args: any):
        self.log_critical("YOU CANNOT EDIT GAME CONFIG, WHAT ARE YOU ON")





GameConfig: GameConfig = GameConfig()


__all__ = ["GameConfig"]
