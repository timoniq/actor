from actor import ABCHandler, ABCResponse, Response


class Handler(ABCHandler):
    async def handle(self, path: str, headers: dict) -> ABCResponse:
        return Response(200, b"Hello world!")
