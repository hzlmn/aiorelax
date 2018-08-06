from aiorelax.server import Server
from yarl import URL
import asyncio

server = Server(
    "http://localhost:5984/", auth="login:pass"
)

loop = asyncio.get_event_loop()


async def main():
    try:
        resp = await server.info()
        print(resp)
    finally:
        await server.close()


if __name__ == "__main__":
    loop.run_until_complete(main())

