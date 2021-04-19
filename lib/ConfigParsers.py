import os
from configparser import ConfigParser

from kivy.uix import screenmanager

import AppInfo
from lib.betterLogger import BetterLogger


class LoggedConfigParser(BetterLogger, ConfigParser):
    def get(self, *args: any, **kwargs: any) -> str:
        result: str = str(super(LoggedConfigParser, self).get(*args, **kwargs))
        if "raw" not in kwargs:
            self.log_debug("Got result", result, "from ini path", args[0], "|",
                           args[1], ". Called with args", args, kwargs)
        return result

    def read(self, *args: any, **kwargs: any) -> list[str]:
        self.log_debug("Loading config file", *args[0], "with args", *args, **kwargs)
        super(LoggedConfigParser, self).read(*args, **kwargs)


class PathConfigParser(LoggedConfigParser):
    def get(self, *args: any, **kwargs: any) -> str:
        result: str = str(super(PathConfigParser, self).get(*args, **kwargs))
        path = os.path.join(AppInfo.resources_dir, result)
        if "raw" not in kwargs:
            self.log_debug("Got result", path, "from ini path", args[0], "|",
                            args[1], ". Called with args", args, kwargs)
        return path


class ExtendedConfigParser(LoggedConfigParser):
    def get(self, *args: any, called_by: str = "MainScript", **kwargs: any) -> str:
        result = str(super(ExtendedConfigParser, self).get(*args, **kwargs))
        if "raw" not in kwargs:
            self.log_debug("Got result", result, "from ini path", args[0], "|",
                            args[1], ". Called by", called_by, "with args", args, kwargs)
        return result

    def getpath(self, *args: any, **kwargs: any) -> str:
        path = self.get(*args, **kwargs, called_by="getpath")
        return os.path.join(AppInfo.resources_dir, path)

    def getkivytranition(self, *args: any, **kwargs: any) -> str:
        transition_str = self.get(*args, **kwargs, called_by="getkivytranition")
        transition = screenmanager.__dict__[transition_str]()
        self.log_trace("Transition is", transition)
        return transition