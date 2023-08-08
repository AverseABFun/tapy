"""Recieving messages on a multiplayer game"""

import json
from txtadv.multiplayer import SERVER
import txtadv
import asyncio
import requests

class RecieveEvent(txtadv.Event):
    """This event is used to trigger something when a event is recieved"""
    def __init__(self, event: type):
        super(self,RecieveEvent).__init__()
        asyncio.ensure_future(self.listenFor(event))
    async def listenFor(self, event: type):
        if not event==txtadv.Event:
            raise TypeError("event is incorrect type, expected txtadv.Event")
        while True:
            data = requests.get(SERVER + "/event/" + event.__name__)
            if json.loads(data).response is not None:
                self.trigger(data=json.loads(data), event=event)
