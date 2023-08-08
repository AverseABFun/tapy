"""Recieving messages on a multiplayer game"""
from txtadv.multiplayer import SERVER
import txtadv
import asyncio
import requests
import json

class RecieveEvent(txtadv.Event):
    def __init__(self, event: type):
        super(self,RecieveEvent).__init__()
        asyncio.ensure_future(self.listenFor(event))
    async def listenFor(self, event: type):
        if not event==txtadv.Event:
            raise TypeError("event is incorrect type, expected txtadv.Event")
        while True:
            data = requests.get(SERVER + "/event/" + event.__name__)
            if json.loads(data).response!=None:
                self.trigger(data=json.loads(data))