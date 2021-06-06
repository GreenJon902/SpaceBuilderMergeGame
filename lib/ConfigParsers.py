from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from kivy.uix.screenmanager import TransitionBase


import json
import os
from configparser import ConfigParser

from kivy.uix import screenmanager

import AppInfo
from lib.betterLogger import BetterLogger


class LoggedConfigParser(ConfigParser, BetterLogger):
    def __init__(self, *args, **kwargs):
        BetterLogger.__init__(self)
        ConfigParser.__init__(self, *args, **kwargs)

    def get(self, *args: any, **kwargs: any) -> str:
        result: str = str(ConfigParser.get(self, *args, **kwargs))
        if "raw" not in kwargs:
            self.log_config("Got result", result, "from ini path", args[0], "|",
                                args[1], ". Called with args", args, kwargs)
        return result

    def read(self, *args: any, **kwargs: any):
        self.log_debug("Loading config file", *args[0], "with args", *args)
        ConfigParser.read(self, *args, **kwargs)


class PathConfigParser(LoggedConfigParser):
    def get(self, *args: any, **kwargs: any) -> str:
        result: str = str(LoggedConfigParser.get(self, *args, **kwargs))
        path = os.path.join(AppInfo.resources_dir, result)
        if "raw" not in kwargs:
            self.log_config("Got result", path, "from ini path", args[0], "|",
                                args[1], ". Called with args", args, kwargs)
        return path


class ExtendedConfigParser(LoggedConfigParser):
    def get(self, *args: any, called_by: str = "MainScript", **kwargs: any) -> str:
        result = str(LoggedConfigParser.get(self, *args, **kwargs))
        if "raw" not in kwargs:
            self.log_config("Got result", result, "from ini path", args[0], "|",
                                args[1], ". Called by", called_by, "with args", args, kwargs)
        return result

    def getpath(self, *args: any, **kwargs: any) -> str:
        path = self.get(*args, **kwargs, called_by="getpath")
        return os.path.join(AppInfo.resources_dir, path)

    def getkivytranition(self, *args: any, **kwargs: any) -> TransitionBase:
        transition_str = self.get(*args, **kwargs, called_by="getkivytranition")
        transition = screenmanager.__dict__[transition_str]()
        self.log_config("Transition is", transition)
        return transition

    def getdict(self, *args: any, **kwargs: any) -> any:
        string = self.get(*args, **kwargs, called_by="getdict").replace("'", '\"')
        return json.loads(string)




def value_from_list_of_keys(array, keys, i=0):
    if len(keys) == i:
        return array
    else:
        return value_from_list_of_keys(array[keys[i]], keys, i+1)


def set_from_list_of_keys(array, keys, to, i=0):
    if len(keys) - 1 == i:
        array[keys[i]] = to
    else:
        set_from_list_of_keys(array[keys[i]], keys, to, i+1)


def del_from_list_of_keys(array, keys, i=0):
    if len(keys) - 1 == i:
        del array[keys[i]]
    else:
        del_from_list_of_keys(array[keys[i]], keys, i+1)


class JSONParser(BetterLogger):
    array: dict = {}
    path: str = ""

    def __init__(self, path: str):
        BetterLogger.__init__(self)

        self.path = path

        self.log_debug("Loading file", path)
        self.array = json.load(open(path))

    def save(self):
        self.log_debug("Saving file", self.path)
        json.dump(self.array, open(self.path, "w"), indent=4)
        self.log_config("Saved")

    def _get(self, *args):
        return value_from_list_of_keys(self.array, args)

    def get(self, *args: any, called_by: str = "MainScript") -> any:
        result = self._get(*args)

        self.log_config("Got result", result, "from path", args, ". Called by", called_by, "with args", args)
        return result


    def set(self, *args: any, to: any = None):
        if to is None:
            raise ValueError("argument to should be set to a value and should not be None")

        else:
            set_from_list_of_keys(self.array, args, to)
            self.log_config("Set", args, "to", to)



    def getpath(self, *args: any) -> str:
        path = self.get(*args, called_by="getpath")
        return os.path.join(AppInfo.resources_dir, path)


    def getkivytranition(self, *args: any) -> str:
        transition_str = self.get(*args, called_by="getkivytranition")
        transition = screenmanager.__dict__[transition_str]()
        self.log_config("Transition is", transition)
        return transition


    def getlist(self, *args: any) -> list:
        return list(self.get(*args, called_by="getlist"))


    def getfloat(self, *args: any) -> float:
        return float(self.get(*args, called_by="getfloat"))

    def getint(self, *args: any) -> int:
        return int(self.get(*args, called_by="getint"))

    def getbool(self, *args: any) -> bool:
        return bool(self.get(*args, called_by="t"))

    def remove(self, *args: any):
        del_from_list_of_keys(self.array, args)



class GameDataJSONParser(JSONParser):
    """
    A nice wrapper class with some functions to help with saving game data like configuring inventory and dealing with
    that array!
    """
    def add_to_inventory(self, item_id: str, amount: int = 1):
        if item_id in self.array["inventory"]:
            self.array["inventory"][item_id] += amount

        else:
            self.array["inventory"][item_id] = amount

        self.log_config("Added", amount, str(item_id) + "(s)", "to inventory")

    def move_to_inventory(self, building_id: int):
        str_building_id = str(building_id)

        self.add_to_inventory(self.array["placed_buildings"][str_building_id]["type"], 1)
        self.array["placed_buildings"].pop(str_building_id)

        self.log_config("Moved", str_building_id, "from placed to inventory")

    def move_to_placed_buildings(self, building_type: str):
        self.array["inventory"][str(building_type)] -= 1
        if self.array["inventory"][str(building_type)] == 0:
            self.array["inventory"].pop(str(building_type))

        from graphics.spaceBuilderMergeGameScreenManager import get_screen
        layout = get_screen("BaseBuildScreen").ids["base_layout"]
        layout.add_building_with_id(building_type)

        self.log_config("Moved", building_type, "from inventory to place buildings")

    def set_building_info(self, building_id: int, building_save_values: dict[str, any]):
        self.array["placed_buildings"][str(building_id)] = building_save_values

        self.log_config("Set building info for", building_id, "to", building_save_values)


__all__ = ["PathConfigParser", "JSONParser", "GameDataJSONParser", "ExtendedConfigParser", "LoggedConfigParser"]
