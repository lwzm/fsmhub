FROM python:slim-stretch

WORKDIR /home/

RUN pip install fsm-hub gunicorn loguru psycopg2-binary \
    && rm -rf /root/.cache

COPY .gunicorn database.yaml ./
EXPOSE 1024
CMD [ "gunicorn", "-c", ".gunicorn", "fsm_hub" ]
