#!/usr/bin/env python3

import collections

from asyncio import Future
from typing import Dict, List, Tuple

from fastapi import FastAPI, HTTPException, Request

from . import core

waits: Dict[str, List[Tuple[Future, Request]]] = collections.defaultdict(list)
app = FastAPI()


@app.post("/new/{state}", status_code=201)
def _(state: str, data: dict = {}):
    return core.new(state, data)


@app.post("/lock/{state}")
def _(state: str):
    try:
        return core.lock(state)
    except core.NotAllowed as e:
        raise HTTPException(400, e.args[0])
    except core.NotFound:
        raise HTTPException(404)


@app.post("/transit/{id}/{state}", status_code=204)
def _(id: int, state: str, data: dict = {}):
    try:
        core.transit(id, state, data)
    except core.NotFound:
        raise HTTPException(404)
    except core.NotAllowed as e:
        raise HTTPException(403, " -> ".join(e.args))


@app.get("/{id}")
def _(id: int):
    try:
        return core.info(id)
    except core.NotFound:
        raise HTTPException(404)


def main():
    pass


if __name__ == '__main__':
    main()
