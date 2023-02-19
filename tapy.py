class Room:
    def __init__(self, name, desc, id, exits, items=[]):
      self.name = name
      self.desc = desc
      self.id = id
      self.exits = exits
      self.items = items
    def __repr__(self):
      return f'TA.Room(name={self.name}, desc={self.desc}, id={self.id}, exits={self.exits})'
  
class Object:
  def __init__(self, name: str, sdesc: str, ldesc: str, id: str, location):
    self.name = name
    self.sdesc = sdesc
    self.ldesc = ldesc
    self.id = id
    self.loc = location
  @property
  def location(self): return self.loc
  def move(self, newloc):
    self.loc = newloc
class Item(Object): pass
class Player(Object):
  def __init__(self, startloc):
    super(Player, self).__init__("player", "", "", "p1p", startloc)
    self.inventory = Room("Inventory", "How did you get here?", "p1i",[])


class World:
    def __init__(self, start, cmds):
      self.start = start
      self.cmds = cmds