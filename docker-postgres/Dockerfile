FROM python:slim-stretch

WORKDIR /home/

RUN pip install --no-cache-dir fsm-hub gunicorn loguru psycopg2-binary redis \
    && find /usr/local/lib/ -name __pycache__ | xargs rm -r

COPY .gunicorn ./
ENV REDIS ""
EXPOSE 1024
CMD [ "gunicorn", "-c", ".gunicorn", "fsm_hub.app" ]
