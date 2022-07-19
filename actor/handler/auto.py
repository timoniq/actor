from .abc import ABCHandler, Request
from actor.response import ABCResponse


class AutoHandler(ABCHandler):
    async def undefined(self, request: Request) -> ABCResponse:
        pass

    async def handle(self, request: Request) -> ABCResponse:
        for name in dir(self):
            if name.startswith("handler_"):
                element = getattr(self, name)
                resp = element(request)
                if not resp:
                    continue
                resp = await resp
                if not resp:
                    continue
                return resp

        return await self.undefined(request)
