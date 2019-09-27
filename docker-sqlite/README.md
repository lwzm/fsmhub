# fsm-hub docker image

```
touch db
docker run --rm -p 1024:1024 -v $PWD/db:/home/db lwzm/fsm-hub:sqlite
```
