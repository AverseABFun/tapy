"""The command-related stuff in tapy."""
from location import get_loc_from_num as _get_loc_from_num
from messaging import error, info, tcolored, setinfomode, NOORIGIN, ORIGIN


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
    setinfomode(NOORIGIN)
    info(player.loc.name + ": " + player.loc.desc + "\n", player)
    if len(player.loc.items) > 0:
        info("There is ", player)
    for i in player.loc.items:
        info(tcolored(i.name,'blue'), player)
    info("\n", player)
    nones = 0
    for i in player.loc.exits:
        nones = nones + int(not i)
    if len(player.loc.exits) == 1 and nones != len(player.loc.exits):
        info("There is an exit ", player)
    elif len(player.loc.exits) > 1 and nones != len(player.loc.exits):
        info("There are exits ", player)
    for index, val in enumerate(player.loc.exits):
        if val:
            loc = _get_loc_from_num(index)
            res = ''
            if loc == 'up':
                loc = 'above you'
                loc = tcolored(loc,'green')
                res = loc
            elif loc == 'down':
                loc = 'below you'
                loc = tcolored(loc,'green')
                res = loc
            else:
                loc = tcolored(loc,'green')
                res = 'to the ' + loc
            if index == len(player.loc.exits) - 1:
                res = 'and ' + res + tcolored('.','grey')
            else:
                res = res + tcolored(', ','grey')
            info(res, player)
    info("\n", player)
    setinfomode(ORIGIN)

def examine(inp, _world, player):
    """Examine an item."""
    inp = inp.replace("examine","",1)
    if (not inp in player.inventory.items) and (not inp in player.loc):
        error("There's no object with that name!\n", player)


globalcmds = [
    Command("look", look, "Look around the room"),
    Command("examine", examine, "Examine an item")
]
