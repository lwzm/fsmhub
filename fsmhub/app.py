#!/usr/bin/env python3

from asyncio import Future
from collections import defaultdict, deque
from typing import Dict, List, Tuple, Deque

from fastapi import FastAPI, HTTPException, Request

from . import core

waitings: Dict[
    str, Deque[Tuple[Future, Request]]
] = defaultdict(deque)
app = FastAPI()


async def notice(token):
    lst = waitings[token]
    while lst:
        future, request = lst.popleft()
        if not await request.is_disconnected():
            future.set_result("ok")
            break
        future.set_result("disconnected")


@app.post("/new/{state}", status_code=201)
async def _(state: str, data: dict = {}) -> int:
    id = core.new(state, data)
    await notice(state)
    return id


@app.post("/lock/{state}")
async def _(state: str, request: Request, wait: bool = False) -> dict:
    while True:
        try:
            return core.lock(state)
        except core.NotAllowed as e:
            raise HTTPException(400, e.args[0])
        except core.NotFound:
            if not wait:
                raise HTTPException(404, f"{state} is not found")
            future = Future()
            waitings[state].append((future, request))
            if await future == "disconnected":
                return {}  # this request has gone, return any has no meaning
            continue


@app.post("/transit/{id}/{state}", status_code=204)
async def _(id: int, state: str, data: dict = {}) -> None:
    try:
        core.transit(id, state, data)
        await notice(state)
    except core.NotFound:
        raise HTTPException(404)
    except core.NotAllowed as e:
        raise HTTPException(403, " -> ".join(e.args))


@app.get("/list-locked")
def _() -> List[dict]:
    return core.list_locked()


@app.get("/list/{state}")
def _(state: str) -> List[dict]:
    return core.list_available(state)

@app.get("/{id}")
def _(id: int) -> dict:
    try:
        return core.info(id)
    except core.NotFound:
        raise HTTPException(404)



def main():
    pass


if __name__ == '__main__':
    main()
