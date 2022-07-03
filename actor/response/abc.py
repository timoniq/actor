import typing
from abc import ABC, abstractmethod


class ABCResponse(ABC):
    charset = "utf-8"
    content_type = "text/plain"

    def with_charset(self, charset: str) -> "ABCResponse":
        self.charset = charset
        return self

    def with_content_type(self, content_type: str) -> "ABCResponse":
        self.content_type = content_type
        return self

    @abstractmethod
    def form(self) -> typing.Iterator[dict]:
        pass
