import asyncio
import operator
import warnings

import aiohttp
from yarl import URL

from .client import Client
from .database import Database
from .helpers import match_version


class Server:

    couchdb_version = None

    def __init__(self, base_url="http://localhost:5984/", auth=None):
        self.auth = auth
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

    async def version(self):
        if self.couchdb_version is not None:
            return self.couchdb_version

        info = await self.info()
        self.couchdb_version = info["version"]

        return self.couchdb_version

    def database(self, name):
        return Database(self.client(name))

    async def stats(self):
        resp = await self.client.get("_stats")
        return await resp.json()

    async def active_tasks(self):
        resp = await self.client.get("_active_tasks")
        return await resp.json()

    async def uuids(self, count=None):
        params = {}
        if count is not None:
            params["count"] = count

        resp = await self.client.get("_uuids", params=params)
        return await resp.json()

    async def membership(self):
        resp = await self.client.get("_membership")
        return await resp.json()

    @match_version("1.6.1", compare=operator.lt)
    async def stats(self):
        raise NotImplementedError

    @match_version("2.0.0")
    async def cluster_setup(self, feed=None, timeout=None, heartbeat=None, since=None):
        feed_values = ("normal", "longpool", "continuous", "eventsource")
        params = {}
        if feed is not None:
            if feed not in feed_values:
                raise ValueError
            params["feed"] = feed
        if timeout is not None:
            params["timeout"] = timeout
        if heartbeat is not None:
            params["heartbeat"] = heartbeat
        if since is not None:
            params["since"] = since

        resp = await self.client.get("_db_updates", params=params)

    async def close(self):
        await self.client.close()
