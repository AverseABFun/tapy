"""The messaging/error components of tapy."""
from inspect import stack

from termcolor import colored

def error(message, target):
    """Print an error to the target."""
    target.stream.write(colored(stack()[1].function + ": " + message, 'red'))


def info(message, target):
    """Print an info message. to the target"""
    target.stream.write(colored(stack()[1].function + ": " + message, 'grey'))


def warning(message, target):
    """Print an warning message to the target."""
    target.stream.write(colored(stack()[1].function + ": " + message, 'orange'))
