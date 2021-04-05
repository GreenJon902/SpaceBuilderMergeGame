import os
from kivy.logger import Logger as _Logger

from AppInfo import log_class_length


class BetterLogger:
    def log_debug(self, *args):
        _Logger.debug(str(self.__class__.__name__) + ": " + "".join([str(arg) for arg in args]))

    def log_info(self, *args):
        _Logger.info(str(self.__class__.__name__) + ": " + "".join([str(arg) for arg in args]))

    def log_warning(self, *args):
        _Logger.warning(str(self.__class__.__name__) + ": " + "".join([str(arg) for arg in args]))

    def log_critical(self, *args):
        _Logger.critical(str(self.__class__.__name__) + ": " + "".join([str(arg) for arg in args]))


def redo_logger_formatting():
    from kivy.logger import formatter_message, COLOR_SEQ, COLORS, RESET_SEQ
    import logging

    class ColoredFormatter(logging.Formatter):

        def __init__(self, msg, use_color=True):
            logging.Formatter.__init__(self, msg)
            self.use_color = use_color

        def format(self, record):
            try:
                msg = record.msg.split(':', 1)
                if len(msg) == 2:
                    record.msg = '[%-64s]%s' % (msg[0], msg[1])
            except:
                pass
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

    print(_Logger)
    print(_Logger.handlers)
    print(_Logger.handlers[2])
    print(use_color, color_fmt)

    formatter = ColoredFormatter(color_fmt, use_color=use_color)
    print(formatter)

    _Logger.handlers[2].setFormatter(formatter)
