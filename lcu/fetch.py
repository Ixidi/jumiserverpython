import sys

from lcu.lcu import Lcu


def fetch_lcu():
    if sys.platform == "win32":
        # TODO fetch from process
        try:
            with open('C:\\Riot Games\\League of Legends\\lockfile', 'r') as f:
                components = f.readline().split(":")
            return Lcu("127.0.0.1", components[2], components[3])
        except FileNotFoundError as e:
            raise e
    else:
        raise SystemError(f'{sys.platform} system is not supported')
