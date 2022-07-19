from actor import ABCHandler, ABCResponse, Response, Request


class Handler(ABCHandler):
    async def handle(self, request: Request) -> ABCResponse:
        return Response(200, b"Hello world!")
