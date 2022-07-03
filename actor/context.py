from actor.response import ABCResponse

MOBILE_AGENTS = list(
    map(
        str.lower, ["Android", "webOS", "iPhone", "iPad", "BlackBerry", "Windows Phone"]
    )
)


class Context:
    def __init__(self, rec, send):
        self.rec = rec
        self._send = send

    async def send(self, response: "ABCResponse"):
        for msg in response.form():
            await self._send(msg)
