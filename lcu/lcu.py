from lcu.gateway import LcuGateway
from lcu.rest import LcuRest


class Lcu:

    def __init__(self, host, port, password):
        self._rest = LcuRest(host, port, password)
        self._gateway = LcuGateway(host, port, password)

    def rest(self):
        return self._rest

    def gateway(self):
        return self._gateway

