from .abc import ABCHandler
from actor.response import ABCResponse


class AutoHandler(ABCHandler):
    async def undefined(self, path: str, headers: dict) -> ABCResponse:
        pass

    async def handle(self, path: str, headers: dict) -> ABCResponse:
        for name in dir(self):
            if name.startswith("handler_"):
                element = getattr(self, name)
                resp = element(path, headers)
                if not resp:
                    continue
                resp = await resp
                if not resp:
                    continue
                return resp

        return await self.undefined(path, headers)
