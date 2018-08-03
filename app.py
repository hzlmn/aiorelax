from aiorelax.client import Client
from yarl import URL
import asyncio

client = Client(URL("http://localhost:5984/"))

loop = asyncio.get_event_loop()


async def main():
    resp = await client.get("_all_dbs")
    print(resp)


if __name__ == "__main__":
    loop.run_until_complete(main())
