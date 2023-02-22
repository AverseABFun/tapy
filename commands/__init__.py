"""The command-related stuff in tapy."""
from location import get_loc_from_num as _get_loc_from_num
from messaging import error


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

    def __call__(self, *args):
        self.func(*args)


def look(_inp, _world, player):
    """Look around from the perspective of the Player passed in."""
    print(player.loc.name + ": " + player.loc.desc)
    if len(player.loc.items) > 0:
        print("There is ", end="")
    for i in player.loc.items:
        print(i.name, end="")
    print()
    nones = 0
    for i in player.loc.exits:
        nones = nones + int(not i)
    if len(player.loc.exits) == 1 and nones != len(player.loc.exits):
        print("There is an exit ", end="")
    elif len(player.loc.exits) > 1 and nones != len(player.loc.exits):
        print("There are exits ", end="")
    for index, val in enumerate(player.loc.exits):
        if val:
            loc = _get_loc_from_num(index)
            res = ''
            if loc == 'up':
                res = 'above you'
            elif loc == 'down':
                res = 'below you'
            else:
                res = 'to the ' + loc
            if index == len(player.loc.exits) - 1:
                res = 'and ' + res + '.'
            else:
                res = res + ', '
            print(res, end='')
    print()

def examine(inp, _world, player):
    """Examine an item."""
    inp = inp.replace("examine","",1)
    if not inp in player.inventory.items and not inp in player.loc:
        error("There's no object with that name!", player)


globalcmds = [
    Command("look", look, "Look around the room")
]
