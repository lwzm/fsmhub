FROM alpine:3.11

LABEL maintainer="lwzm@qq.com"

ENV DB=postgres://postgres@postgres
EXPOSE 80

CMD [ "uvicorn", "fsmhub:app", "--loop=asyncio", "--host=0.0.0.0", "--port=80" ]

RUN apk add --no-cache libpq python3 \
    && apk add --no-cache --virtual .build-deps gcc libc-dev make postgresql-dev python3-dev \
    && pip3 install --no-cache-dir fastapi h11 click pony \
    && pip3 install --no-cache-dir --no-dependencies uvicorn fsmhub==4.5 \
    && apk del .build-deps \
    && pip3 uninstall -y setuptools pip \
    && cd /usr/lib/python3* \
    && python3 -OO -m compileall -q -b -f . \
    && rm -rf site-packages/*.*-info \
    && find . -name __pycache__ | xargs rm -rf \
    && find . -name '*.py' -delete
