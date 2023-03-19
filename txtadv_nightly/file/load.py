"""Load any object from a pickled object"""
import os
import inspect
import sys
import marshal
import pickle
import json
from .. import messaging
from .. import __init__ as txtadv
savepath = os.path.dirname(inspect.getfile(txtadv)) + "/saves"


class Call:
    """The class that's used to make this module callable"""

    def single_load(self, item):
        """Load a single item"""
        try:
            return json.loads(item)
        except TypeError:
            try:
                return marshal.loads(item)
            except TypeError:
                try:
                    return marshal.loads(item.__code__)
                except AttributeError:
                    try:
                        return pickle.loads(item)
                    #pylint: disable-next=duplicate-code
                    except pickle.PicklingError:
                        messaging.error(
                            #pylint: disable-next=line-too-long
                            f"Sorry, we found an {item.__class__.__name__} with the name/signature {item} that is an invalid object for the world storage system. This means that you aren't basing it on an Object, an Item, a Player, a Room, or an Entity. Please make it be based on one of those.\n",
                            sys.stdout)
                        return bytes()

    def __call__(self, filename):
        try:
            #pylint: disable-next=consider-using-with
            file = pickle.load(open(filename+".save",'rb'))
        except (FileNotFoundError, IsADirectoryError, TypeError, pickle.UnpicklingError):
            #pylint: disable-next=line-too-long
            messaging.error(f"Attempted load of invalid save/nonexistant save {filename}!\n",sys.stdout)
            return
        if file.__class__.__name__ != "dict":
            messaging.error(f"Attempted load of invalid save {filename}!\n",sys.stdout)
            return
        if file["__VERSION__"] != txtadv.__VERSION__:
            #pylint: disable-next=line-too-long
            file_version = file["__VERSION__"] # I do this instead of putting it in the f-string directly because for some reason if I do, pylint and python get VERY mad
            #pylint: disable-next=line-too-long
            messaging.error(f"Attempted load of save {filename} which has a file version of {file_version}, but this copy of txtadv is still on version {txtadv.__VERSION__}!\n",sys.stdout)
        copy = {}
        for ite in file.items():
            copy[ite] = self.single_load(ite)


sys.modules[__name__] = Call()
