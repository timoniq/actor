from .abc import ABCResponse
import typing
import json


class Response(ABCResponse):
    def __init__(self, status_code: int, body: typing.Union[bytes, dict, str]):
        self.body = body
        self.status_code = status_code

        if isinstance(body, dict):
            self.body = json.dumps(self.body)

        if isinstance(body, str):
            self.body = self.body.encode(self.charset)

    def get_body(self) -> bytes:
        if isinstance(self.body, bytes):
            return self.body
        raise TypeError("Invalid body type")

    def form(self) -> typing.List[dict]:
        yield from [
            {
                "type": "http.response.start",
                "status": self.status_code,
                "headers": [
                    [
                        b"content-type",
                        f"{self.content_type}; charset={self.charset}".encode(
                            self.charset
                        ),
                    ]
                ],
            },
            {"type": "http.response.body", "body": self.get_body()},
        ]
