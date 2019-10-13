FROM python:alpine

LABEL maintainer="lwzm@qq.com"

WORKDIR /home/

RUN pip install --no-cache-dir fsm-hub \
    && touch db \
    && find /usr/local/lib/ -name '*.pyc' -delete

COPY database.yaml ./
EXPOSE 1024
CMD [ "fsm-hub" ]
