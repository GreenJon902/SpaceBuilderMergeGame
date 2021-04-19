import os

from kivy.logger import Logger as _Logger, WHITE, COLOR_SEQ


class BetterLogger:
    __log_name_prefix__: str = ""
    __log_name__: str = "You have a serious bug, you shouldn't be able to see this"
    __log_name_suffix__: str = ""

    def __init__(self, *args: any, prefix: str = None, name: str = None, suffix: str = None, **kwargs):
        super(BetterLogger, self).__init__(*args, **kwargs)

        if prefix is not None:
            self.__log_name_prefix__ = str(prefix)

        if name is not None:
            self.__log_name__ = str(name)
        else:
            self.__log_name__ = str(self.__class__.__name__)

        if suffix is not None:
            self.__log_name_suffix__ = str(suffix)

    def log_trace(self, *args: any):
        _Logger.debug(str(self.__log_name_prefix__) + str(self.__log_name__) + str(self.__log_name_suffix__) +
                      ": " + " ".join([str(arg) for arg in args]) + "" + "|||DEEP DEBUG|||")

    def log_debug(self, *args: any):
        _Logger.debug(str(self.__log_name_prefix__) + str(self.__log_name__) + str(self.__log_name_suffix__) +
                      ": " + " ".join([str(arg) for arg in args]))

    def log_info(self, *args: any):
        _Logger.info(str(self.__log_name_prefix__) + str(self.__log_name__) + str(self.__log_name_suffix__) +
                     ": " + " ".join([str(arg) for arg in args]))

    def log_warning(self, *args: any):
        _Logger.warning(str(self.__log_name_prefix__) + str(self.__log_name__) + str(self.__log_name_suffix__) +
                        ": " + " ".join([str(arg) for arg in args]))

    def log_critical(self, *args: any):
        _Logger.critical(str(self.__log_name_prefix__) + str(self.__log_name__) + str(self.__log_name_suffix__) +
                         ": " + " ".join([str(arg) for arg in args]))


def redo_logger_formatting():
    from AppInfo import log_class_length
    from kivy.logger import formatter_message, COLOR_SEQ, COLORS, RESET_SEQ, ColoredFormatter as _ColoredFormatter, \
        WHITE
    import logging
    from kivy import logger as kvLogger

    ENABLE_DEEP_DEBUG = False  # Requires normal debug to be enabled

    if os.environ.get("ENABLE_DEEP_DEBUG") is not None:
        ENABLE_DEEP_DEBUG = bool(os.environ.get("ENABLE_DEEP_DEBUG"))
    else:
        try:
            if logging.ENABLE_DEEP_DEBUG:
                ENABLE_DEEP_DEBUG = True

        except AttributeError:
            pass

    class ColoredFormatter(_ColoredFormatter):
        def format(self, record: logging.LogRecord) -> str:
            try:
                msg: (str, str) = record.msg.split(':', 1)
                if len(msg) == 2:
                    record.msg = ('[%-' + str(log_class_length) + 's]%s') % (msg[0], msg[1])
            except Exception:
                print("redo_logger_formatting broke!")
            levelname: str = record.levelname
            if record.levelno == kvLogger.LOG_LEVELS["trace"]:
                levelname: str = 'TRACE'
                record.levelname = levelname
            if self.use_color and levelname in COLORS:
                if "|||DEEP DEBUG|||" in record.msg:
                    levelname_color: str = (
                            str(COLOR_SEQ % (30 + WHITE)) + "[DEEP DEBUG")
                    record.levelname = levelname_color
                    record.msg = record.msg.replace("|||DEEP DEBUG|||", "")
                else:
                    levelname_color: str = (
                            str(COLOR_SEQ % (30 + COLORS[levelname])) + "[" + levelname)
                    record.levelname = levelname_color
            return logging.Formatter.format(self, record)

    class DeepDebugFilter(logging.Filter):
        def filter(self, record):
            if not ENABLE_DEEP_DEBUG and "|||DEEP DEBUG|||" in record.msg:
                return False

            else:
                return True

    use_color: bool = (
            (
                    os.environ.get("WT_SESSION") or
                    os.environ.get("COLORTERM") == 'truecolor' or
                    os.environ.get('PYCHARM_HOSTED') == '1' or
                    os.environ.get('TERM') in (
                        'rxvt',
                        'rxvt-256color',
                        'rxvt-unicode',
                        'rxvt-unicode-256color',
                        'xterm',
                        'xterm-256color',
                    )
            ) and os.environ.get('KIVY_BUILD') not in ('android', 'ios')
    )
    if not use_color:
        color_fmt: str = formatter_message(
            '[%(levelname)-7s] %(message)s', use_color)

    else:
        color_fmt: str = formatter_message(
            RESET_SEQ + '%(levelname)-18s] %(message)s', use_color)

    formatter: ColoredFormatter = ColoredFormatter(color_fmt, use_color=use_color)

    _Logger.handlers[2].setFormatter(formatter)
    _Logger.addFilter(DeepDebugFilter())
