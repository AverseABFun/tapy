class Room:

  def __init__(self, name, desc, id, exits, items=[]):
    self.name = name
    self.desc = desc
    self.id = id
    self.exits = exits
    self.items = items

  def __repr__(self):
    return f'Room(name={self.name}, desc={self.desc}, id={self.id}, exits={self.exits})'


class Object:

  def __init__(self, name: str, sdesc: str, ldesc: str, id: str, location):
    self.name = name
    self.sdesc = sdesc
    self.ldesc = ldesc
    self.id = id
    self.loc = location

  @property
  def location(self):
    return self.loc

  def move(self, newloc):
    self.loc = newloc


class Item(Object):

  def move(self, newloc):
    super(Item, self).move(newloc)
    newloc.items.append(self)


class Player(Object):

  def __init__(self, startloc):
    super(Player, self).__init__("player", "", "", "p1p", startloc)
    self.inventory = Room("Inventory", "How did you get here?", "p1i", [])

  def pickup(self, item: Item):
    item.move(self.inventory)


class Command:

  def __init__(self, name, func, desc):
    self.name = name
    self.func = func
    self.desc = desc


class World:

  def __init__(self, start, cmds):
    self.start = start
    self.cmds = cmds
    self.player = Player(start)

  def run(self, prompt="> "):
    while True:
      inp = input(self.player.loc.name + prompt)
      for cmd in self.cmds:
        if inp.startswith(cmd.name):
          cmd.func(inp)
