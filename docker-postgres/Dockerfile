FROM alpine as base

LABEL maintainer="lwzm@qq.com"

WORKDIR /tmp/pip

RUN apk add gcc musl-dev libev-dev postgresql-dev python3-dev \
    && pip3 install wheel \
    && pip3 wheel bjoern psycopg2

FROM alpine

COPY --from=base /tmp/pip .

RUN apk add --no-cache libev libpq python3 \
    && pip3 install --no-cache-dir  *.whl fsm-hub \
    && rm *.whl \
    && find /usr/lib/ -name '*.pyc' -delete

WORKDIR /home/
ENV NOTICE="" PORT=80
EXPOSE 80

CMD [ "fsm-hub" ]
