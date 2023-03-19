"""Tests for txtadv"""
from os import system
from txtadv import Room, Item, Entity, World
if __name__ == "__main__":
    try:
        try:
            import pylint
        except ValueError:
            system("find . -name '*.pyc' -delete")
            import pylint
    except ImportError:
        system("pip install pylint")
        import pylint
    system("pylint txtadv_nightly/*.py txtadv_nightly/*/*.py")
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
