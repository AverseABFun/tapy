"""A feature-rich text adventure framework in Python."""
import sys
import os
from typing import Callable, Any, List
import commands
from messaging import info, setinfomode, no_origin, origin, error as err


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
    """A Event that is triggered when an Object is moved(Includes the player picking it up)."""


class UseEvent(Event):
    """A Event that is triggered when an Item is used."""


class EnterEvent(Event):
    """A Event that is triggered when an Player enters a Room."""


class Object:
    """A base Object. Do not use, instead use Item or Player."""
    events = {"move": MoveEvent()}
    default_flags = {}

    def __init__(self, name: str, sdesc: str, ldesc: str, location):
        self.name = name
        self.sdesc = sdesc
        self.ldesc = ldesc
        self.loc = location
        self.iname = name
        self.flags = self.__class__.default_flags

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
        try:
            self.__class__.events[event_name].add_subscriber(subscriber)
        except KeyError as exc:
            sys.tracebacklimit = -1
            raise ValueError(f"Unknown event `{event_name}`") from exc


class Item(Object):
    """An Item. Doesn't do much by default, although it can."""
    events = Object.events.update({"use": UseEvent()})
    default_flags = {"consume_on_use": False, "pickup_to_examine": True}
    def __init__(self, name: str, sdesc: str, ldesc: str, location):
        super().__init__(name, sdesc, ldesc, location)
        location.items.append(self)

    def move(self, newloc):
        super().move(newloc)
        newloc.items.append(self)

    def use(self):
        """Use the item"""
        self.__class__.events["use"].trigger(self.iname)


class Room:
    """The Room class can contain a number of items and have up to 6 exits:
    up, down, north, south, east, and west."""
    events = {"enter": EnterEvent()}

    def __init__(self, name: str, desc: str, exits, items) -> None:
        self.name = name
        self.iname = name
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

    def __contains__(self, key):
        for i in self.items:
            if key in (i.iname, i):
                return True
        for i in self.exits:
            if key in (i.iname, i):
                return True
        return False


class Player(Object):
    """A Player. Don't use, instead use World.create_player or just instance a new World."""
    events = Object.events.update({})
    default_flags = {}

    def __init__(self, startloc: Room, instream, outstream, colored=True) -> None:
        super().__init__("player", "", "", startloc)
        self.inventory = Room("Inventory", "How did you get here?", [], [])
        self.instream = instream
        self.outstream = outstream
        self.colored = colored

    def pickup(self, item: Item):
        """Pickup an item."""
        item.move(self.inventory)


class Entity(Player):
    """An Entity. Can be described as a scripted player."""

    def __init__(self, startloc: Room, file_name: str):
        self.colored = False
        with open(file_name, 'r', encoding='ascii') as file:
            with open(os.devnull, 'w', encoding='ascii') as null:
                super().__init__(startloc, file, null)

    def exec_from_file(self, file_name):
        """Set the file executed from"""
        with open(file_name, 'r', encoding='ascii') as file:
            self.instream = file

    def tick(self, world):
        """Tickes the entity and makes it perform an action."""
        self.exec(self.instream.readline(), world)

    def exec(self, instruction, world):
        """Executes an instruction for this Entity."""
        cmd_count = 0
        for cmd in world.cmds:
            for alias in cmd.aliases:
                if instruction.startswith(alias):
                    setinfomode(origin)
                    cmd(instruction, world, self)
                    found = True
                    break
                cmd_count += 1
            cmd_count -= len(cmd.aliases)
            if not found:
                cmd_count += 1
            else:
                break
        if cmd_count == len(world.cmds):
            err("Invalid command. Run 'help' to get a list of commands.\n",sys.stdout)


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
        self.players = [Player(start, sys.stdin, sys.stdout)]
        self.entities = []

    def run(self, prompt: str = "> ") -> None:
        """Runs the game"""
        while True:
            for player in self.players:
                setinfomode(no_origin)
                info(player.loc.name + prompt,player)
                player.outstream.flush()
                sys.tracebacklimit = -1
                inp = player.instream.readline().replace("\n", "")
                sys.tracebacklimit = 1000
                cmd_count = 0
                found = False
                for cmd in self.cmds:
                    for alias in cmd.aliases:
                        if inp.startswith(alias):
                            setinfomode(origin)
                            cmd(inp, self, player)
                            found = True
                            break
                        cmd_count += 1
                    cmd_count -= len(cmd.aliases)
                    if not found:
                        cmd_count += 1
                    else:
                        break
                if cmd_count == len(self.cmds):
                    err("Invalid command. Run 'help' to get a list of commands.\n",player)
            for i in self.entities:
                i.tick(self)

    def create_player(self, instream, outstream) -> None:
        """Creates a new Player in this World."""
        self.players.append(Player(self.room, instream, outstream))

    def add_entity(self, entity: Entity) -> None:
        """Adds an Entity to this World."""
        self.entities.append(entity)


if __name__ == "__main__":
    testroom = Room("testroom", "a room", [], [])
    testroom.exits = [testroom,testroom,testroom,testroom,testroom,testroom]
    testitem = Item("a test item", "a test item", "what were you expecting?", testroom)
    testworld = World(testroom)
    testworld.run()
