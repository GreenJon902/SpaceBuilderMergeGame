from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass


from lib.betterLogger import BetterLogger



logger = BetterLogger(name="GlobalEvents")


class GlobalEvents:
    bindings: dict[str, list] = {}

    @classmethod
    def bind(cls, **kwargs):
        for event_name, function in kwargs.items():
            cls.check_binding(event_name)

            cls.bindings[event_name].append(function)
            logger.log_deep_debug(function, "was bound to event '", event_name, "'")

    @classmethod
    def register(cls, event_name: str):
        cls.bindings[event_name] = list()
        logger.log_debug("Event '", event_name, "' has been created")

    @classmethod
    def dispatch(cls, event_name: str, *args, **kwargs):
        cls.check_binding(event_name)
        for function in cls.bindings[event_name]:
            function(*args, **kwargs)

    @classmethod
    def check_binding(cls, event_name: str):
        if event_name not in cls.bindings:
            cls.register(event_name)


__all__ = ["GlobalEvents"]
