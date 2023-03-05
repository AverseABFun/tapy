"""The command-related stuff in tapy."""
from location import get_loc_from_num as _get_loc_from_num
from messaging import error, info, setinfomode, no_origin, origin
from color import colored


class Command:
    """A command, such as 'look' or 'examine'."""

    #pylint: disable-next=too-many-arguments
    def __init__(self, name: str, func, desc: str, ldesc: str, aliases=None):
        self.name = name
        self.func = func
        self.desc = desc
        self.ldesc = ldesc
        if aliases is None:
            aliases = []
        self.aliases = [name] + aliases

    def help(self):
        """Returns the help string for this command"""
        return f"{self.name} - {self.desc}"

    def __str__(self):
        return self.help()

    def __repr__(self):
        return self.help()

    def __call__(self, *args):
        self.func(*args)


#pylint: disable-next=too-many-branches
def look(inp, _world, player):
    """Look around from the perspective of the Player passed in."""
    inp = inp.replace("look", "", 1).strip()
    if inp.split(" ")[0] == "at":
        inp = inp.replace("at", "", 1).strip()
        examine("examine " + inp, _world, player)
        return
    setinfomode(no_origin)
    info(player.loc.name + ": " + player.loc.desc + "\n", player)
    if len(player.loc.items) > 0:
        info("There is ", player)
    for i in player.loc.items:
        info(colored(i.name, 'blue'), player)
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
                loc = colored(loc, 'green')
                res = loc
            elif loc == 'down':
                loc = 'below you'
                loc = colored(loc, 'green')
                res = loc
            else:
                loc = colored(loc, 'green')
                res = 'to the ' + loc
            if index == len(player.loc.exits) - 1:
                res = 'and ' + res + colored('.', 'grey')
            else:
                res = res + colored(', ', 'grey')
            info(res, player)
    info("\n", player)
    setinfomode(origin)


def examine(inp, _world, player):
    """Examine an item."""
    inp = inp.replace("examine ", "", 1)
    item = None
    for i in player.inventory.items:
        if i.name == inp:
            item = i
    for i in player.loc.items:
        if i.name == inp:
            item = i
    if not item:
        error("There's no object with that name!\n", player)
        return
    setinfomode(no_origin)
    info(colored(item.name + ': ' + item.ldesc, 'yellow') + '\n', player)
    setinfomode(origin)


def tahelp(inp, world, player):
    """The help command. Named 'tahelp' so that it won't override the builtin function 'help'"""
    inp = inp.replace("help", "", 1).strip()
    setinfomode(no_origin)
    if inp != "":
        for i in world.cmds:
            if i.name == inp:
                info(colored(i.name + ": " + i.ldesc + '\n', 'blue'), player)
                setinfomode(origin)
                return
        error(
            "There's no command with that name! Run 'help' to get a list of commands.\n",
            player)
    for index, val in enumerate(world.cmds):
        if index % 2 == 0:
            info(colored(val.help() + '\n', 'yellow'), player)
        elif index % 2 == 1:
            info(colored(val.help() + '\n', 'blue'), player)
    setinfomode(origin)


def move(_inp, _world, _player):
    """Go in a specific direction"""


def say(inp, world, player):
    """Say something in the room you are in"""
    inp = inp.replace("say", "", 1).strip()
    world.chatEvent.trigger(inp, player.name, local=player.loc)


def announce(inp, world, player):
    """Announce something to the entire World"""
    inp = inp.replace("announce", "", 1).strip()
    world.chatEvent.trigger(inp, player.name, local=None)


globalcmds = [
    Command("help", tahelp, "Get help on the commands",
            "It's the help command"),
    Command("look", look, "Look around the room",
            "Look at the room that the current player is in"),
    Command("examine", examine, "Examine an item",
            "Examine an item closely to get more info"),
    Command("go", move, "Go in a direction", "Go in a certain direction",
            ["move"]),
    Command(
        "say", say, "Say something to the room you are currently in",
        "Unlike 'announce', it will only say something to the room you are currently in"
    ),
    Command("announce", announce, "Announce something to the entire World",
            "Unlike 'say', this command says something to the entire World")
]
