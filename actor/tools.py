import typing
import re
from actor.context import MOBILE_AGENTS
from .handler.abc import Request


def regex_path(paths: typing.Union[str, typing.List[str]]):
    paths = paths if isinstance(paths, list) else [paths]
    patterns = [re.compile(path) for path in paths]

    def wrapper(func):
        def call_wrapper(self, request: Request, *args):
            matches = [re.match(pattern, request.path) for pattern in patterns]
            matches = list(filter(bool, matches))
            if matches:
                return func(self, request, *(matches[0].groups()), *args)
            return None

        return call_wrapper

    return wrapper


def resolve_mobile(func):
    def call_wrapper(self, request: Request, *args, **kwargs):
        mobile = any(
            [
                agent.lower() in (request.headers.get(b"user-agent", b"")).decode().lower()
                for agent in MOBILE_AGENTS
            ]
        )
        return func(self, request, *args, **kwargs, mobile=mobile)

    return call_wrapper
