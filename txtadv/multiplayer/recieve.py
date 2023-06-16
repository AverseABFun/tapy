"""Recieving messages on a multiplayer game(VERY WIP) (Doesn't work)"""
import taw_proto.taw as taw_proto
import txtadv
class RecieveEvent(txtadv.Event):
    def __init__(self, event):
        super(self,RecieveEvent).__init__()
        self.listenFor(event)
    def listenFor(self, event):
        if type(event).__name__ != "txtadv.multiplayer.taw_proto.taw":
            raise TypeError(f"variable 'event' is from an invalid module {type(event).__name__}, expected to be from txtadv.multiplayer.taw_proto.taw")