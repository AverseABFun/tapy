"""Tests for txtadv"""
import txtadv

if __name__ == "__main__":
    testroom = txtadv.Room("testroom", "a room", [], [])
    testroom.exits = [
        testroom, testroom, testroom, testroom, testroom, testroom
    ]
    testitem = txtadv.Item("a test item", "a test item", "what were you expecting?",
                    testroom)
    testworld = txtadv.World(testroom, author="Arthur Beck", name="Test Game", desc="A test game")

    testworld.run()
