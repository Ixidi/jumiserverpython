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

    def _check_listener(self, listener, event):
        if listener.uri[-1] == "/":
            check = event['uri'].startswith(listener.uri)
        else:
            check = listener.uri == event['uri']
        return check and listener.event_type == event['eventType'].lower()

    async def start(self):
        while True:
            event = await self._gateway.receive_event()
            for listener in [x for x in self._listeners if self._check_listener(x, event)]:
                await listener.handler(event['data'])
