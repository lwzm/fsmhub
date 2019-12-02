#!/usr/bin/env python3

from os import environ
from requests import Session, codes


hub = environ.get("HUB", "http://localhost:1024")
http = Session()


def get_config():
    rsp = http.get(f"{hub}/")
    rsp.raise_for_status()
    return rsp.json()


def get(id):
    rsp = http.get(f"{hub}/{id}")
    rsp.raise_for_status()
    return rsp.json()


def new(state, initial_data: dict = None):
    rsp = http.post(f"{hub}/new/{state}", json=initial_data)
    rsp.raise_for_status()


def lock(state):
    rsp = http.post(f"{hub}/lock/{state}")
    if rsp.status_code == codes.NOT_FOUND:
        return
    rsp.raise_for_status()  # hub is gone or logic is broken, so just exit
    return rsp.json()


def transit(id, next_state, patch_data: dict = None):
    rsp = http.post(f"{hub}/transit/{id}/{next_state}", json=patch_data)
    rsp.raise_for_status()


if __name__ == '__main__':
    print(get_config())
    new("x")
    id = lock("x")["id"]
    transit(id, "xxx")
    print(get(id))
