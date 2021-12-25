import asyncio

from jumi.eventhandler import EventHandler
from jumi.module.championselect import apply_champion_select_module
from jumi.module.lobby import apply_lobby_module
from jumi.module.queue import apply_queue_module


class Jumi:

    def __init__(self, lcu):
        self.lcu = lcu
        self.event_handler = EventHandler(lcu.gateway())

    async def start(self):
        apply_lobby_module(self)
        apply_queue_module(self)
        apply_champion_select_module(self)
        gateway_loop = asyncio.create_task(self.lcu.gateway().open())
        event_handler_loop = asyncio.create_task(self.event_handler.start())
        await asyncio.gather(gateway_loop, event_handler_loop)
