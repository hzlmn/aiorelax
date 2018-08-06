import asyncio
import logging
from functools import partialmethod

import aiohttp
import async_timeout
from yarl import URL

logger = logging.getLogger(__name__)


class Client:
    def __init__(
        self, base_url, loop=None, session=None, verify_ssl=True, timeout=10, auth=None
    ):
        if not isinstance(base_url, URL):
            raise TypeError("base_url should be instance of URL")

        if loop is None:
            loop = asyncio.get_event_loop()

        self.loop = loop
        self.base_url = base_url
        self.timeout = timeout

        if isinstance(auth, str):
            auth = aiohttp.BasicAuth(*auth.split(":"))

        if auth is not None and not isinstance(auth, aiohttp.BasicAuth):
            raise TypeError("auth should be str or aiohttp.BasicAuth")

        self.auth = auth

        if session is None:
            session = aiohttp.ClientSession(
                auth=auth,
                raise_for_status=True,
                connector=aiohttp.TCPConnector(
                    use_dns_cache=True, loop=loop, verify_ssl=verify_ssl
                ),
            )
        self.session = session

        self.headers = {}

    def __call__(self, path=None):
        base_url = self.base_url / path
        return type(self)(
            base_url,
            loop=self.loop,
            session=self.session,
            auth=self.auth,
            timeout=self.timeout,
        )

    async def close(self):
        await self.session.close()

    async def request(self, method, url=None, params=None, data=None):
        url = self.base_url / url

        async with async_timeout.timeout(self.timeout):
            try:
                response = await self.session.request(
                    method, url, params=params, data=data, headers=self.headers
                )

                return response
            except aiohttp.ClientError as exc:
                logger.exception(exc, exc_info=exc)
                raise

    get = partialmethod(request, "GET")

    head = partialmethod(request, "HEAD")

    post = partialmethod(request, "POST")

    put = partialmethod(request, "PUT")

    delete = partialmethod(request, "DELETE")

    # A special method that can be used to copy documents and objects.
    copy = partialmethod(request, "COPY")
