# FSMHUB

Finite State Machine storage hub

### Install
```
pip install fsmhub
```

### Start service
```
uvicorn fsmhub:app
```

docker
```
docker run -p 1024:80 lwzm/fsmhub
```


### Use it

3 HTTP APIs:

* `POST /new/<STATE>`, optional json payload for init custom data
* `POST /lock/<STATE>`
* `POST /transit/<ID>/<NEW-STATE>`, optional json payload for patch custom data

### Examples
```
$ http post :1024/new/a
HTTP/1.1 201 Created
Connection: Keep-Alive
content-length: 0
content-type: application/json; charset=UTF-8



$ http post :1024/lock/a
HTTP/1.1 200 OK
Connection: Keep-Alive
content-length: 71
content-type: application/json; charset=UTF-8

{
    "data": {},
    "id": 1,
    "state": "a",
    "ts": "2019-09-23 10:38:44.234700"
}


$ http post :1024/transit/1/b
HTTP/1.1 204 No Content
Connection: Keep-Alive
content-length: 0
content-type: application/json; charset=UTF-8

```


### TODOS

* [x] postgres/sqlite trigger for log changes
* [x] long polling
* [ ] docs
