"""A feature-rich text adventure framework in Python."""
import sys
from typing import Callable, Any, List
import commands


class _CONSTANTS:

    def global_cmds(self):
        """The global/default commands"""
        return commands.globalcmds

    def function_to_make_pylint_happy_ignore(self):
        """ignore this"""


_CONSTANTS = _CONSTANTS()


class Subscriber:
    """A Subscriber to an Event"""

    def __init__(self, func: Callable[[Any], Any]):
        self.func = func
        self.events = []

    def __call__(self, *args, **kwargs):
        self.func(*args, **kwargs)

    def __set__(self, key, val):
        self.events.append(val)

    def add_event(self, event):
        """Add an Event to this Subscriber"""
        self.events.append(event)


class Event:
    """An Event that can have multiple Subscribers"""

    def __init__(self):
        self.subscribers = []

    def add_subscriber(self, subscriber: Subscriber):
        """Add an subscriber to this Event"""
        self.subscribers.append(subscriber)
        subscriber.add_event(self)

    def trigger(self, *args, **kwargs):
        """Trigger this Event with one or more arguments"""
        for sub in self.subscribers:
            sub(*args, **kwargs)


class MoveEvent(Event):
    """A Event that is triggered when an Object is moved."""


class UseEvent(Event):
    """A Event that is triggered when an Item is used."""


class EnterEvent(Event):
    """A Event that is triggered when an Player enters a Room."""


class Object:
    """A base Object. Do not use, instead use Item or Player."""
    events = {"move": MoveEvent()}

    def __init__(self, name: str, sdesc: str, ldesc: str, location):
        self.name = name
        self.sdesc = sdesc
        self.ldesc = ldesc
        self.loc = location
        self.iname = name

    @property
    def location(self):
        """The location of this Object"""
        return self.loc

    def move(self, newloc):
        """Moves this Object to a different Room"""
        self.loc = newloc
        self.__class__.events["move"].trigger(self.iname)

    def on_event(self, event_name: str, subscriber: Subscriber):
        """Makes subscriber be triggered when event_name is triggered."""
        error = False
        try:
            self.__class__.events[event_name].add_subscriber(subscriber)
        except KeyError:
            sys.tracebacklimit = -1
            error = True
        if error:
            raise ValueError(f"Unknown event `{event_name}`")


class Item(Object):
    """An Item. Doesn't do much by default, although it can."""
    events = Object.events.update({"use": UseEvent()})

    def move(self, newloc):
        super().move(newloc)
        newloc.items.append(self)

    def use(self):
        """Use the item"""
        self.__class__.events["use"].trigger(self.iname)


class Room:
    """The Room class can contain a number of items and have 
    up to 6 exits - up, down, north, south, east, and west."""
    events = {"enter": EnterEvent()}

    def __init__(self, name: str, desc: str, exits, items) -> None:
        self.name = name
        self.desc = desc
        self.exits = exits
        self.items = items

    def move_item(self, item: Item, newloc):
        """Moves an Item to a different Room if it is in this Room"""
        if item in self.items:
            item.move(newloc)
            self.items.remove(item)

    def remove_item(self, item: Item):
        """Removes an Item from this Room"""
        if item in self.items:
            self.items.remove(item)

    def on_event(self, event_name: str, subscriber: Subscriber):
        """Makes subscriber be triggered when event_name is triggered."""
        error = False
        try:
            self.__class__.events[event_name].add_subscriber(subscriber)
        except KeyError:
            sys.tracebacklimit = -1
            error = True
        if error:
            raise ValueError(f"Unknown event `{event_name}`")

    def enter(self, player):
        """Trigger the enter event with the Player passed"""
        self.__class__.events["enter"].trigger(player)


class Player(Object):
    """The player. Don't use, instead use World.create_player or just instance a new World."""

    def __init__(self, startloc: Room) -> None:
        super().__init__("player", "", "", startloc)
        self.inventory = Room("Inventory", "How did you get here?", [], [])

    def pickup(self, item: Item):
        """Pickup an item."""
        item.move(self.inventory)


class World:
    """The World class. Contains a starting room, a list of commands, and at least one player."""

    def __init__(
            self,
            start: Room,
            cmds: List[commands.Command] = _CONSTANTS.global_cmds) -> None:
        self.room = start
        if callable(cmds):
            self.cmds = cmds()
        else:
            self.cmds = cmds
        self.players = [Player(start)]

    def run(self, prompt: str = "> ") -> None:
        """Runs the game"""
        while True:
            inp = input(self.players[0].loc.name + prompt)
            for cmd in self.cmds:
                if inp.startswith(cmd.name):
                    cmd(inp)

    def create_player(self) -> None:
        """Creates a new Player in this World."""
        self.players.append(Player(self.room))
