#!/usr/bin/env python3

from datetime import datetime, timedelta
from pony import orm
from .entities import Fsm, db


prefix_locked = "locked-"


class NotFound(Warning): pass
class NotAllowed(Warning): pass


@orm.db_session
def new(state, data={}):
    Fsm(state=state, data=data)


@orm.db_session
def lock(state):
    if state.startswith(prefix_locked):
        raise NotAllowed(f"prefix '{prefix_locked}' is not allowed")
    ts = datetime.now() - timedelta(seconds=300)
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
def transit(id, state, data_patch=None):
    i = Fsm.get_for_update(id=id)
    if not i:
        raise NotFound(id)
    if not i.state.startswith(prefix_locked):
        raise NotAllowed(i.state, state)
    i.state = state
    i.ts = datetime.now()
    if data_patch:
        i.data.update(data_patch)


def _init_this():
    #orm.sql_debug(True)
    from os.path import abspath
    from yaml import safe_load
    try:
        options = safe_load(open("database.yaml"))
    except FileNotFoundError:
        options = {"provider": "sqlite", "filename": ":memory:"}
    fn = options.get("filename")
    if fn and fn != ":memory:":
        options["filename"] = abspath(fn)  # $CWD/filename
    db.bind(**options)
    db.generate_mapping(create_tables=True)


if __name__ == '__main__':
    db.bind('sqlite', filename=':memory:')
    db.generate_mapping(create_tables=True)
else:
    _init_this()
