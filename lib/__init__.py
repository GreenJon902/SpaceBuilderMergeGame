# From https://stackoverflow.com/a/32922362/11411477 bc i dont know stuff like this well
import functools


def ignore_args(func, *args, **kwargs):
    @functools.wraps(func)
    def newfunc(*_args, **_kwargs):
        return func(*args, **kwargs)
    return newfunc
