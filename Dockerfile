FROM alpine

LABEL maintainer="lwzm@qq.com"

ENV DB=postgres://postgres@postgres
EXPOSE 80

CMD [ "uvicorn", "fsmhub:app", "--host=0.0.0.0", "--port=80" ]

RUN apk add --no-cache python3 libpq \
    && apk add --no-cache --virtual .build-deps gcc libc-dev make postgresql-dev python3-dev \
    && python3 -m ensurepip \
    && pip3 install fsmhub psycopg2 \
    && find /usr/ -name __pycache__ | xargs rm -rf \
    && apk del .build-deps
