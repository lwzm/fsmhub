FROM alpine

LABEL maintainer="lwzm@qq.com"

WORKDIR /root/

RUN apk add --no-cache python3 \
    && pip3 install --no-cache-dir fsm-hub \
    && touch db \
    && find /usr/lib/ -name '*.pyc' -delete

COPY database.yaml .sqliterc ./

ENV PORT=80
EXPOSE 80

CMD [ "fsm-hub" ]
