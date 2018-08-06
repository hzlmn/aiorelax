import aiohttp
import asyncio
from yarl import URL

from .client import Client


class Server:
    def __init__(self, base_url="http://localhost:5984/", auth=None):
        self.base_url = URL(base_url)
        self.client = Client(self.base_url, auth=auth)

    async def all_dbs(self):
        resp = await self.client.get("_all_dbs")
        resp.raise_for_status()
        return await resp.json()

    async def info(self):
        resp = await self.client.get("")
        resp.raise_for_status()
        return await resp.json()

    async def close(self):
        await self.client.close()
