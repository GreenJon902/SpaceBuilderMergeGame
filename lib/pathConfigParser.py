import os
from configparser import ConfigParser

import AppInfo


class PathConfigParser(ConfigParser):
    def get(self, *args, **kwargs) -> str:
        path = super(PathConfigParser, self).get(*args, **kwargs)
        return os.path.join(AppInfo.resources_dir, path)
