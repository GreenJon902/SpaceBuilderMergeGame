import os

from kivy.logger import Logger as _Logger


class BetterLogger:
    __log_name_prefix__ = ""
    __log_name_suffix__ = ""

    @classmethod
    def log_trace(cls, *args):
        _Logger.trace(cls.__log_name_prefix__ + str(cls.__class__.__name__) + cls.__log_name_suffix__ + ": " + " ".join([str(arg) for arg in args]))

    @classmethod
    def log_debug(cls, *args):
        _Logger.debug(cls.__log_name_prefix__ + str(cls.__class__.__name__) + cls.__log_name_suffix__ + ": " + " ".join([str(arg) for arg in args]))

    @classmethod
    def log_info(cls, *args):
        _Logger.info(cls.__log_name_prefix__ + str(cls.__class__.__name__) + cls.__log_name_suffix__ + ": " + " ".join([str(arg) for arg in args]))

    @classmethod
    def log_warning(cls, *args):
        _Logger.warning(cls.__log_name_prefix__ + str(cls.__class__.__name__) + cls.__log_name_suffix__ + ": " + " ".join([str(arg) for arg in args]))

    @classmethod
    def log_critical(cls, *args):
        _Logger.critical(cls.__log_name_prefix__ + str(cls.__class__.__name__) + cls.__log_name_suffix__ + ": " + " ".join([str(arg) for arg in args]))


def redo_logger_formatting():
    from AppInfo import log_class_length
    from kivy.logger import formatter_message, COLOR_SEQ, COLORS, RESET_SEQ, ColoredFormatter as _ColoredFormatter
    import logging

    class ColoredFormatter(_ColoredFormatter):
        def format(self, record):
            try:
                msg = record.msg.split(':', 1)
                if len(msg) == 2:
                    record.msg = ('[%-' + str(log_class_length) + 's]%s') % (msg[0], msg[1])
            except Exception as e:
                print("redo_logger_formatting broke!")
            levelname = record.levelname
            if record.levelno == logging.TRACE:
                levelname = 'TRACE'
                record.levelname = levelname
            if self.use_color and levelname in COLORS:
                levelname_color = (
                        COLOR_SEQ % (30 + COLORS[levelname]) + levelname + RESET_SEQ)
                record.levelname = levelname_color
            return logging.Formatter.format(self, record)

    use_color = (
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
        color_fmt = formatter_message(
            '[%(levelname)-7s] %(message)s', use_color)

    else:
        color_fmt = formatter_message(
            '[%(levelname)-18s] %(message)s', use_color)

    formatter = ColoredFormatter(color_fmt, use_color=use_color)

    _Logger.handlers[2].setFormatter(formatter)
