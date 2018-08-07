import asyncio
from functools import partial, wraps

from .errors import ClientError


def match_version(expected_version):
    def factory(func):
        @wraps(func)
        async def wrapped(*args, **kwargs):
            obj = args[0]
            handler = getattr(obj, "version")
            version = await invoke(handler)
            major, *_ = map(int, version.split("."))
            if major < expected_version:
                raise RuntimeError(
                    "%s not supported by current version of CouchDB v%s"
                    % (func.__name__, version)
                )
            return await func(*args, **kwargs)

        return wrapped

    return factory


async def invoke(func):
    result = func()
    if asyncio.iscoroutine(result):
        result = await result
    return result
