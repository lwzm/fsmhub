FROM alpine

LABEL maintainer="lwzm@qq.com"

ENV FSMHUB_DB_URL=sqlite://data/db
EXPOSE 80

CMD [ "uvicorn", "fsmhub:app", "--host=0.0.0.0", "--port=80" ]

RUN apk add --no-cache python3 \
    && apk add --no-cache --virtual .build-deps gcc libc-dev python3-dev \
    && python3 -m ensurepip \
    && pip3 install --no-cache-dir fastapi httptools click pony \
    && pip3 install --no-cache-dir --no-dependencies uvicorn fsmhub==4.7 \
    && apk del .build-deps \
    && pip3 uninstall -y setuptools pip \
    && mkdir -p data \
    && echo 'pragma synchronous = off;' >~/.sqliterc \
    && cd /usr/lib/python3* \
    && rm -r ensurepip \
    && python3 -OO -m compileall -q -b -f . \
    && rm -rf site-packages/*.*-info \
    && find . -name __pycache__ | xargs rm -rf \
    && find . -name '*.py' -delete
