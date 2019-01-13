import sys


def no_traceback(func):
    def inner(*args, **kwargs):
        sys.tracebacklimit = 0
        func(*args, **kwargs)
        sys.tracebacklimit = 1000
    return inner
