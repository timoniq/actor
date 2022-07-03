from actor import AutoHandler, ABCResponse, Response


class Handler(AutoHandler):
    async def handle(self, path: str, headers: dict) -> ABCResponse:
        return Response(200, b"Hello world!")
