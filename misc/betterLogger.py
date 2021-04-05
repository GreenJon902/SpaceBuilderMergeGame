from kivy.logger import Logger as _Logger

class BetterLogger:
    def log_debug(self, *args):
        _Logger.debug(str(self.__name__) + ": " + "".join([str(arg) for arg in args]))

    def log_info(self, *args):
        _Logger.info(str(self.__name__) + ": " + "".join([str(arg) for arg in args]))

    def log_warning(self, *args):
        _Logger.warning(str(self.__name__) + ": " + "".join([str(arg) for arg in args]))

    def log_critical(self, *args):
        _Logger.critical(str(self.__name__) + ": " + "".join([str(arg) for arg in args]))


