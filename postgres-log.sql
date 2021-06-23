create or replace function tcp_log() returns trigger language plpython3u as $$
from json import loads

log, plan = "log", "plan"

if log not in SD:
    from tcplog import TcpLog
    SD[log] = TcpLog("172.17.0.1:1111")

if plan not in SD:
    SD[plan] = plpy.prepare("INSERT INTO fsm_history VALUES ($1,$2,$3,$4)",
                              ["integer", "text", "timestamp", "jsonb"])

x = TD['new']
plpy.execute(SD[plan],  [x["id"], x["state"], x["ts"], x["data"]])
x["data"] = loads(x["data"])
SD[log](**x)

return 'OK'
$$;

drop trigger if exists log_fsm on fsm;
create trigger log_fsm
after insert or update
on fsm
for each row
execute procedure tcp_log();

create table if not exists "fsm_history" (
    id integer references fsm (id),
    state character varying(80),
    ts timestamp,
    data jsonb
);
