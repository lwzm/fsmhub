#!/usr/bin/env python3


tpl = """
--drop table {tb};

create table {tb} (
    _ timestamp default now(),
    id integer,
    state varchar(80),
    ts timestamp,
    data jsonb,
    delay interval
);

create index {tb}__ on {tb} (_);
create index {tb}_id on {tb} (id);
""".format

trigger_sql = """
create or replace function fsm_history() returns trigger
language 'plpgsql'
as $$
declare
tb text := 'day_' || lpad(date_part('day', now())::text, 2, '0');
begin
    execute
    format('insert into %s (id, state, ts, data, delay) values ($1, $2, $3, $4, $5)', tb)
    using NEW.id, NEW.state, NEW.ts, NEW.data, NEW.ts - OLD.ts;
    return NEW;
end
$$;

drop trigger tg_fsm_history on fsm;
create trigger tg_fsm_history
    after insert or update on fsm
    for each row execute procedure fsm_history();
"""


def main():
    for i in range(1, 32):
        tb = "day_{:02}".format(i)
        print(tpl(tb=tb))
    print(trigger_sql)


if __name__ == '__main__':
    main()
    """
    ./optional_record_history_postgres.py | psql
    """
