import logging
import os
import re
import sys
import typing
from importlib.machinery import SourceFileLoader

import aiofiles
import uvicorn
import pathlib

from actor import ABCHandler, Response, Context, Request

CURRENT_ABSPATH = str(pathlib.Path().resolve())

replacements: typing.Dict[str, str] = {}

with open("ADDRESSES", "r") as s:
    addresses_raw = s.readlines()
    addresses: typing.List[str] = []

    for address in addresses_raw:
        if not address:
            continue

        address = address.replace("\n", "")
        spl = address.split(" -> ")

        if len(spl) == 2:
            replacements[spl[0]] = spl[1]
        addresses.append(spl[-1])

handlers: typing.Dict[str, ABCHandler] = {}
statics: typing.Dict[str, typing.Dict[str, str]] = {}

for address in addresses:
    ptn = open(address + "/STATIC").read().splitlines()
    address_statics: typing.Dict[str, str] = {}
    for pt in ptn:
        pt = pt.split(" -> ")
        address_statics[pt[0]] = pt[0] if len(pt) == 1 else pt[1]

    statics[address] = address_statics

for address in addresses:
    sys.path.append(address)
    a = SourceFileLoader("app", address + "/app.py").load_module()
    handler = getattr(a, "Handler")
    if not address.startswith("/"):
        setattr(
            handler,
            "getpath",
            lambda *path: CURRENT_ABSPATH + os.sep + address + os.sep + path[-1]
            if not path[-1].startswith("/")
            else path[-1],
        )
    else:
        setattr(
            handler,
            "getpath",
            lambda *path: address + os.sep + path[-1]
            if not path[-1].startswith("/")
            else path[-1],
        )
    if not handler:
        print(f"Unable to load {address}, Handler is undefined")
        continue
    handlers[address] = handler()


async def app(scope, receiver, sender):
    headers = dict(scope.get("headers", ()))
    ctx = Context(receiver, sender)
    host = headers.get(b"host", b"").decode()

    if host in replacements:
        host = replacements[host]

    if host not in handlers:
        response = Response(404, b"Not handling")
        return await ctx.send(response)

    path: str = scope.get("path", "/")

    if path == "/favicon.ico":
        if f"{host}.ico" not in "static":
            logging.warning(f"Favicon for {host} (static/{host}.ico) is undefined")
            response = Response(404, b"")
            await ctx.send(response)
            return

        async with aiofiles.open(f"static/{host}.ico", "rb") as stream:
            data = await stream.read()

        response = Response(200, data)
        await ctx.send(response)

    elif re.match("/static/[^/]+", path):
        p = path.split("/")[-1]

        if p in statics[host]:
            path = statics[host][p]
            j = path.split(" ")

            content_type: typing.Optional[str] = None
            if len(j) == 2:
                content_type = j[1]

            if path not in os.listdir("static"):
                response = Response(404, b"")
                return await ctx.send(response)

            async with aiofiles.open("static/" + path, "rb") as stream:
                data = await stream.read()

            response = Response(200, data)
            if content_type:
                response.content_type = content_type
            await ctx.send(response)
        else:
            response = Response(404, b"")
            await ctx.send(response)

    else:
        request = Request(path, headers, scope, receiver, sender)
        response = await handlers[host].handle(request)
        if response:
            await ctx.send(response)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080)
