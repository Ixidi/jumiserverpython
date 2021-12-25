import dataclasses
from typing import Callable


@dataclasses.dataclass
class Listener:
    uri: str
    event_type: str
    handler: Callable[[dict], None]


class EventHandler:

    def __init__(self, gateway):
        self._gateway = gateway
        self._listeners = []

    def listener(self, uri, event_type='update'):
        def wrap(func):
            self._listeners.append(Listener(uri, event_type, func))
            return func
        return wrap

    async def start(self):
        while True:
            event = await self._gateway.receive_event()
            for listener in [x for x in self._listeners if x.uri == event['uri'] and x.event_type == event['eventType'].lower()]:
                listener.handler(event['data'])
