"""Tests for txtadv"""
from os import system
from txtadv_nightly import Room, Item, Entity, World
import txtadv_nightly.color
import subprocess
if __name__ == "__main__":
    try:
        try:
            import pylint
        except ValueError:
            system("find . -name '*.pyc' -delete")
            import pylint
    except ImportError:
        system("pip install pylint")
        try:
            import pylint
        except ValueError:
            system("find . -name '*.pyc' -delete")
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
    txtadv_nightly.color.background_color('blue')
    testworld.run()
