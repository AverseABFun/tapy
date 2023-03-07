from tapy import Room, Item, Entity, World
from os import system
if __name__ == "__main__":
    system("pip install pylint")
    system("pylint */*.py */*/*.py")
    testroom = Room("testroom", "a room", [], [])
    testroom.exits = [
        testroom, testroom, testroom, testroom, testroom, testroom
    ]
    testitem = Item("a test item", "a test item", "what were you expecting?",
                    testroom)
    testentity = Entity(testroom, "test.entity")
    testworld = World(testroom)
    testworld.add_entity(testentity)
    testworld.run()