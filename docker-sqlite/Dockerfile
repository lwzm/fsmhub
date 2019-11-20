FROM python:alpine

LABEL maintainer="lwzm@qq.com"

WORKDIR /root/

RUN pip install --no-cache-dir fsm-hub \
    && touch db \
    && find /usr/local/lib/ -name '*.pyc' -delete

COPY database.yaml .sqliterc ./
EXPOSE 1024
CMD [ "fsm-hub" ]
