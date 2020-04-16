FROM alpine

LABEL maintainer="lwzm@qq.com"

RUN apk add --no-cache python3 \
    && apk add --no-cache --virtual .build-deps gcc libc-dev make python3-dev \
    && pip3 install --no-cache-dir fsm-hub \
    && apk del .build-deps \
    && touch db \
    && find /usr/lib/ -name '*.pyc' -delete

ENV PORT=80 DB=sqlite://db
EXPOSE 80

CMD [ "fsm-hub" ]
