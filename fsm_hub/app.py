#!/usr/bin/env python3

import json

from falcon import Request, Response, API, HTTPNotFound, HTTPForbidden, HTTPBadRequest, HTTP_CREATED

from .core import new, lock, transit, info, NotFound, NotAllowed, notice_base_url


class Index:
    def on_get(self, req: Request, resp: Response):
        resp.body = json.dumps({
            "notice": notice_base_url,
        })


class InitNew:
    def on_post(self, req: Request, resp: Response, state):
        data = json.load(req.stream) if req.content_length else {}
        new(state, data)
        resp.status = HTTP_CREATED


class LockOne:
    def on_post(self, req: Request, resp: Response, state):
        try:
            item = lock(state)
        except NotAllowed as e:
            raise HTTPBadRequest(description=e.args[0])
        except NotFound:
            raise HTTPNotFound
        resp.body = json.dumps(item, default=str, ensure_ascii=False)


class TransitLocked:
    def on_post(self, req: Request, resp: Response, id, state):
        data = json.load(req.stream) if req.content_length else None
        try:
            transit(id, state, data)
        except NotFound:
            raise HTTPNotFound
        except NotAllowed as e:
            raise HTTPForbidden(description=" -> ".join(e.args))


class Info:
    def on_get(self, req: Request, resp: Response, id):
        try:
            item = info(id)
        except NotFound:
            raise HTTPNotFound
        resp.body = json.dumps(item, default=str, ensure_ascii=False)


application = API()
application.add_route('/', Index())
application.add_route('/new/{state}', InitNew())
application.add_route('/lock/{state}', LockOne())
application.add_route('/transit/{id:int}/{state}', TransitLocked())
application.add_route('/{id:int}', Info())


def main():
    import os
    port = int(os.environ.get("PORT", 1024))
    try:
        from bjoern import run
        run(application, "", port)
    except ImportError:
        pass
    from wsgiref.simple_server import make_server
    make_server("", port, application).serve_forever()


if __name__ == '__main__':
    main()
