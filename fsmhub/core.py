#!/usr/bin/env python3

from datetime import datetime, timedelta
from typing import Any, Dict, List, Union
from os import getenv

from pony import orm

from .entities import Fsm, db


prefix_locked = getenv("FSMHUB_PREFIX_LOCKED") or "."
ageing_time = timedelta(seconds=float(getenv("FSMHUB_AGEING_SECONDS") or 300))

JSONDict = Dict[str, Any]


class NotFound(Warning):
    pass


class NotAllowed(Warning):
    pass


def new(state: str, data: JSONDict = {}) -> int:
    with orm.db_session:
        i = Fsm(state=state, data=data)
    return i.id


@orm.db_session
def lock(state: str) -> JSONDict:
    if state.startswith(prefix_locked):
        raise NotAllowed(f"{prefix_locked}* is not allowed: {state}")
    ts = datetime.now() - ageing_time
    i = orm.select(
        i for i in Fsm if i.ts > ts and i.state == state
    ).order_by(Fsm.ts).for_update(skip_locked=True).first()
    if not i:
        raise NotFound(state)
    prev_info = i.to_dict()
    i.state = f"{prefix_locked}{i.state}"
    i.ts = datetime.now()
    return prev_info


@orm.db_session
def transit(id: int, state: str, data_patch: JSONDict = None):
    if state.startswith(prefix_locked):
        raise NotAllowed(f"{prefix_locked}* is not allowed: {state}")
    i = Fsm.get_for_update(id=id)
    if not i:
        raise NotFound(id)
    if not i.state.startswith(prefix_locked):
        raise NotAllowed(i.state, state)
    i.state = state
    i.ts = datetime.now()
    if data_patch is not None:
        i.data.update(data_patch)


@orm.db_session
def info(id) -> JSONDict:
    try:
        return Fsm[id].to_dict()
    except orm.ObjectNotFound:
        raise NotFound(id)


@orm.db_session
def list_locked() -> List[JSONDict]:
    q = orm.select(
        (i.id, i.ts, i.state) for i in Fsm if i.state.startswith(prefix_locked)
    ).order_by(2)
    return [{"id": id, "ts": ts, "state": state} for id, ts, state in q]


@orm.db_session
def list_available(state) -> List[JSONDict]:
    ts = datetime.now() - ageing_time
    q = orm.select(
        (i.id, i.ts) for i in Fsm if i.ts > ts and i.state == state
    ).order_by(2)
    return [{"id": id, "ts": ts} for id, ts in q]


def parse_db(url: str) -> Dict[str, Union[str, int, None]]:
    """See:
    https://docs.ponyorm.org/database.html#binding-the-database-object-to-a-specific-database
    """
    from os.path import abspath
    from urllib.parse import urlparse, unquote
    u = urlparse(url)
    provider = u.scheme
    if provider == "sqlite":
        filename = unquote(u.netloc + u.path)
        if filename != ":memory:":
            filename = abspath(filename)  # $CWD/filename
        return {
            "provider": provider,
            "filename": filename,
            "create_db": True
        }
    auth, _, loc = u.netloc.rpartition("@")
    user, _, password = map(unquote, auth.partition(":"))
    host, _, port = map(unquote, loc.partition(":"))
    port = port and int(port) or None
    database = u.path.lstrip("/")
    if provider == "postgres":
        return {
            "provider": provider,
            "user": user,
            "password": password,
            "host": host,
            "port": port,
            "database": database,
        }
    elif provider == "mysql":
        return {
            "provider": provider,
            "user": user,
            "passwd": password,
            "host": host,
            "port": port,
            "db": database,
        }

    raise ValueError(url)


def _init_this():
    # orm.sql_debug(True)
    db_url = getenv("FSMHUB_DB_URL") or "sqlite://fsmhub.db"
    options = parse_db(db_url)
    db.bind(**options)
    db.generate_mapping(create_tables=True)


if __name__ == '__main__':
    db.bind('sqlite', filename=':memory:')
    db.generate_mapping(create_tables=True)
    print(parse_db("sqlite://test"))
    print(parse_db("mysql://root:password@my:3306/test"))
    print(parse_db("postgres://postgres@postgres"))
else:
    _init_this()
