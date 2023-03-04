"""The messaging/error components of tapy."""
from inspect import FrameInfo
import inspect

from color import colored

NOORIGIN = lambda: [FrameInfo('',0,'','',0,0),FrameInfo('',0,'','',0,0)]
ORIGIN = inspect.stack


def setinfomode(mode):
    """Set the info mode of messaging."""
    inspect.stack = mode


def error(message, target):
    """Print an error to the target."""
    if target.colored:
        target.outstream.write(
            colored(inspect.stack()[1].function + ": " + message, 'red'))
    else:
        target.outstream.write('ERROR: ' + inspect.stack()[1].function + ": " +
                               message)
    target.outstream.flush()


def info(message, target):
    """Print an info message to the target"""
    if target.colored:
        target.outstream.write(
            colored(inspect.stack()[1].function + message, 'grey'))
    else:
        target.outstream.write(inspect.stack()[1].function + ": " + message)
    target.outstream.flush()


def ocolored(message, target, color):
    """Print an colored message to the target if it is supported."""
    if target.colored:
        target.outstream.write(
            colored(inspect.stack()[1].function + ": " + message, color))
    else:
        target.outstream.write(inspect.stack()[1].function + ": " + message)
    target.outstream.flush()

def tcolored(message, color):
    return colored(message, color)
