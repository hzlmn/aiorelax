import asyncio
import operator
from functools import partial, reduce, wraps

from .errors import ClientError


def parse_version(version):
    return version.strip().split(".")


def get_version(version):
    return int("".join(parse_version(version)))


def match_version(expected_version, compare=operator.ge):
    def factory(func):
        @wraps(func)
        async def wrapped(*args, **kwargs):
            obj = args[0]
            handler = getattr(obj, "version")

            version = await handler()
            parsed_version = get_version(version)
            expected = get_version(expected_version)

            if not compare(parsed_version, expected):
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
