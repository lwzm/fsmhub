FROM alpine:3.14

LABEL maintainer="lwzm@qq.com"

EXPOSE 80

ENV PYTHONOPTIMIZE=2 PYTHONDONTWRITEBYTECODE=1

CMD [ "uvicorn", "fsmhub:app", "--host=0.0.0.0", "--port=80" ]

RUN apk add python3 libpq \
    && apk add --virtual .build-deps gcc libc-dev postgresql-dev python3-dev \
    && python3 -m ensurepip \
    && pip3 install --no-cache-dir psycopg2 pymysql pony fastapi uvicorn \
    && pip3 uninstall -y setuptools pip \
    && find /usr/ -name __pycache__ | xargs rm -r \
    && apk del .build-deps \
    && rm -r /var/cache/apk

COPY fsmhub fsmhub
