class Database:
    def __init__(self, client):
        self.client = client

    async def all_docs(self):
        resp = await self.client.get("_all_docs")
        return await resp.json()
