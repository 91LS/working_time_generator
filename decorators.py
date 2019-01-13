import sys


def no_traceback(func):
    def inner(*args, **kwargs):
        sys.tracebacklimit = 0
        return func(*args, **kwargs)
    return inner
