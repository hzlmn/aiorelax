from aiohttp import ClientError

class AiorelaxError(ClientError):
    pass