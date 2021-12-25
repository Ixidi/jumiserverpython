import asyncio
import base64
import json
import pathlib
import ssl

import websockets


class LcuGateway:

    def __init__(self, host, port, password):
        self._url = f'wss://{host}:{port}'
        credentials = base64.b64encode(f'riot:{password}'.encode()).decode()
        self._auth_header = {'Authorization': f'Basic {credentials}'}
        self._ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        localhost_pem = pathlib.Path(__file__).parent.with_name('riotgames.pem')
        self._ssl_context.load_verify_locations(localhost_pem)
        self._queue = asyncio.Queue()
        self._ws = None

    async def open(self):
        async with websockets.connect(self._url, extra_headers=self._auth_header, ssl=self._ssl_context) as ws:
            self._ws = ws
            await ws.send('[5, \"OnJsonApiEvent\"]')
            while True:
                r = await ws.recv()
                if len(r) == 0:
                    continue
                await self._queue.put(json.loads(r)[2])
            self._ws = None

    async def receive_event(self):
        return await self._queue.get()
