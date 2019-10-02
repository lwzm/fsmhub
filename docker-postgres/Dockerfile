FROM python:slim-stretch

WORKDIR /home/

RUN pip install fsm-hub gunicorn loguru psycopg2-binary redis \
    && rm -rf /root/.cache

COPY .gunicorn database.yaml ./
ENV REDIS ""
EXPOSE 1024
CMD [ "gunicorn", "-c", ".gunicorn", "fsm_hub.app" ]
