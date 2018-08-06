import asyncio
import warnings

import aiohttp
from yarl import URL

from .client import Client
from .database import Database


class Server:
    def __init__(self, base_url="http://localhost:5984/", auth=None):
        self.base_url = URL(base_url)
        self.client = Client(self.base_url, auth=auth)

    async def __aiter__(self):
        for db in await self.all_dbs():
            resp = await self.client.get(db)
            yield (await resp.json())

    async def all_dbs(self):
        resp = await self.client.get("_all_dbs")
        return await resp.json()

    async def info(self):
        resp = await self.client.get("")
        return await resp.json()

    def database(self, name):
        return Database(self.client(name))

    async def stats(self):
        resp = await self.client.get("_stats")
        return await resp.json()

    async def active_tasks(self):
        resp = await self.client.get("_active_tasks")
        return await resp.json()

    async def close(self):
        await self.client.close()
