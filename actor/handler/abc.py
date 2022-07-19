import typing

from actor.response import ABCResponse
from abc import ABC, abstractmethod
import dataclasses


@dataclasses.dataclass
class Request:
    path: str
    headers: dict
    scope: dict
    receive: typing.Callable
    send: typing.Callable


class ABCHandler(ABC):
    @abstractmethod
    async def handle(self, request: Request) -> ABCResponse:
        pass

    @staticmethod
    def getpath(path: str) -> str:
        return path
