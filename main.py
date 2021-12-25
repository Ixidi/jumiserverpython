import asyncio

from jumi.jumi import Jumi
from lcu.fetch import fetch_lcu


def main():
    lcu = fetch_lcu()
    if lcu is None:
        raise EnvironmentError("lol is not open")
    try:
        asyncio.gather(asyncio.get_event_loop().run_until_complete(Jumi(lcu).start()), return_exceptions=True)
    except KeyboardInterrupt:
        print("ending...")


if __name__ == '__main__':
    main()
