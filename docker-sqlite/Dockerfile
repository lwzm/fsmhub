FROM python:alpine

WORKDIR /home/

RUN pip install fsm-hub loguru \
    && touch db \
    && rm -rf /root/.cache

COPY database.yaml ./
EXPOSE 1024
CMD [ "fsm-hub" ]
