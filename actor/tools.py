import typing
import re
from actor.context import MOBILE_AGENTS


def regex_path(paths: typing.Union[str, typing.List[str]]):
    paths = paths if isinstance(paths, list) else [paths]
    patterns = [re.compile(path) for path in paths]

    def wrapper(func):
        def call_wrapper(self, p: str, headers: dict, *args):
            matches = [re.match(pattern, p) for pattern in patterns]
            matches = list(filter(bool, matches))
            if matches:
                return func(self, p, headers, *(matches[0].groups()), *args)
            return None

        return call_wrapper

    return wrapper


def resolve_mobile(func):
    def call_wrapper(self, p: str, headers: dict, *args, **kwargs):
        mobile = any(
            [
                agent.lower() in (headers.get(b"user-agent", b"")).decode().lower()
                for agent in MOBILE_AGENTS
            ]
        )
        return func(self, p, headers, *args, **kwargs, mobile=mobile)

    return call_wrapper
