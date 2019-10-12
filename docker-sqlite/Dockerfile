FROM python:alpine

WORKDIR /home/

RUN pip install --no-cache-dir fsm-hub loguru \
    && touch db \
    && find /usr/local/lib/ -name __pycache__ | xargs rm -r

COPY database.yaml ./
EXPOSE 1024
CMD [ "fsm-hub" ]
