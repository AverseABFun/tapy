"""A feature-rich text adventure framework in Python."""


class Object:
    """A base Object. Do not use, instead use Item or Player."""

    def __init__(self, name: str, sdesc: str, ldesc: str, location):
        self.name = name
        self.sdesc = sdesc
        self.ldesc = ldesc
        self.loc = location

    @property
    def location(self):
        """The location of this Object"""
        return self.loc

    def move(self, newloc):
        """Moves this Object to a different Room"""
        self.loc = newloc


class Item(Object):
    """An Item. Doesn't do much by default, although it can."""

    def move(self, newloc):
        super().move(newloc)
        newloc.items.append(self)


class Room:
    """The Room class can contain a number of items and have 
    up to 6 exits - up, down, north, south, east, and west."""

    def __init__(self,
                 name: str,
                 desc: str,
                 exits,
                 items) -> None:
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


class Player(Object):
    """The player. Don't use, instead use World.create_player or just instance a new World."""

    def __init__(self, startloc: Room) -> None:
        super().__init__("player", "", "", startloc)
        self.inventory = Room("Inventory", "How did you get here?", [], [])

    def pickup(self, item: Item):
        """Pickup an item."""
        item.move(self.inventory)


class Command:
    """A command, such as 'look' or 'examine'."""

    def __init__(self, name: str, func, desc: str):
        self.name = name
        self.func = func
        self.desc = desc

    def help(self):
        """Returns the help string for this command"""
        return f"{self.name} - {self.desc}"

    def __str__(self):
        return self.help()

    def __repr__(self):
        return self.help()


class World:
    """The World class. Contains a starting room, a list of commands, and at least one player."""

    def __init__(self, start: Room, cmds) -> None:
        self.room = start
        self.cmds = cmds
        self.players = [Player(start)]

    def run(self, prompt: str = "> ") -> None:
        """Runs the game"""
        while True:
            inp = input(self.players[0].loc.name + prompt)
            for cmd in self.cmds:
                if inp.startswith(cmd.name):
                    cmd.func(inp)

    def create_player(self) -> None:
        """Creates a new Player in this World."""
        self.players.append(Player(self.room))
