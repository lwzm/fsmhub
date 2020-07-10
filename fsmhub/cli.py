#!/usr/bin/env python3

import json

from http import client
from urllib.parse import urlparse


class HTTPError(Exception):
    pass


class Api:
    def __init__(self, url):
        url = urlparse(url)
        if url.scheme == "http":
            self.http = client.HTTPConnection(url.netloc)
        elif url.scheme == "https":
            self.http = client.HTTPSConnection(url.netloc)
        else:
            raise ValueError(url)

    def get(self, id):
        self.http.request("GET", f"/{id}")
        r = self.http.getresponse()
        if r.status > client.NO_CONTENT:
            raise HTTPError(r.status)
        return json.load(r)

    def _post(self, path, data=None):
        body = data and json.dumps(data)
        self.http.request("POST", path, body, headers={"Content-Type": "application/json"})
        r = self.http.getresponse()
        if r.status > client.NO_CONTENT:
            raise HTTPError(r.status)
        o = r.read()
        if o:
            return json.loads(o)

    def new(self, state, initial_data: dict = None):
        return self._post(f"/new/{state}", initial_data)

    def lock(self, state):
        return self._post(f"/lock/{state}?wait=yes")

    def transit(self, id, next_state, patch_data: dict = None):
        return self._post(f"/transit/{id}/{next_state}", patch_data)



if __name__ == '__main__':
    api = Api("http://localhost:8000")
    api.new("x", {"a": 1})
    id = api.lock("x")["id"]
    api.transit(id, "xxx", {"a": 2})
    print(api.get(id))
