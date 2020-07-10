# fsmhub docker image

```
touch db
docker run --rm -p 1024:80 -v $PWD/db:/home/db lwzm/fsmhub:sqlite
```
