from actor.response import ABCResponse
from abc import ABC, abstractmethod


class ABCHandler(ABC):
    @abstractmethod
    async def handle(self, path: str, headers: dict) -> ABCResponse:
        pass
