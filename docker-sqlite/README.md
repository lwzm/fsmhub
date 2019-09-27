# fsm-hub docker image

```
touch db
docker run -d --name fsm-hub -p 1024:1024 -v $PWD/db:/home/db fsm-hub
```
