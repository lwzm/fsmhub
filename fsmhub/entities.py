#!/usr/bin/env python3

from pathlib import Path
from datetime import datetime
from pony.orm import Database, PrimaryKey, Required, Optional, Json, composite_index


db = Database()


@db.on_connect(provider="sqlite")
def _home_sqliterc(_, conn):
    rc = Path.home() / ".sqliterc"
    rc.exists() and conn.executescript(rc.read_text())


class Fsm(db.Entity):
    id = PrimaryKey(int, auto=True)
    state = Required(str, 80)
    ts = Required(datetime, default=datetime.now)
    data = Optional(Json)
    composite_index(ts, state)


if __name__ == '__main__':
    db.bind('sqlite', filename=':memory:')
    db.generate_mapping(create_tables=True)
