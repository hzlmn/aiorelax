import aiohttp
import asyncio
from yarl import URL

from .client import Client


class Server:
    def __init__(self, base_url="http://localhost:5984/"):
        self.base_url = URL(base_url)
        self.client = Client()


    async def all_dbs(self, auth=None):
        resp = await self.client.get("/_all_dbs", auth=auth)
        resp.raise_for_status()
        return await resp.json()
