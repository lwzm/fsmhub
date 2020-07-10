FROM alpine

LABEL maintainer="lwzm@qq.com"

RUN apk add --no-cache libpq python3 \
    && apk add --no-cache --virtual .build-deps gcc libc-dev make postgresql-dev python3-dev \
    && pip3 install --no-cache-dir fsmhub psycopg2 \
    && apk del .build-deps \
    && cd /usr/lib/python3* \
    && python3 -OO -m compileall -q -b -f . \
    && find . -name __pycache__ | xargs rm -rf \
    && find . -name '*.py' -delete

ENV DB=postgres://postgres@postgres
EXPOSE 80

CMD [ "uvicorn", "fsmhub:app", "--host=0.0.0.0", "--port=80" ]
