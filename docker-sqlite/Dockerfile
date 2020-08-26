FROM alpine:3.11

LABEL maintainer="lwzm@qq.com"

ENV DB=sqlite://data/db
EXPOSE 80

CMD [ "uvicorn", "fsmhub:app", "--host=0.0.0.0", "--port=80" ]

RUN apk add --no-cache python3 \
    && pip3 install --no-cache-dir fastapi h11 click pony \
    && pip3 install --no-cache-dir --no-dependencies uvicorn fsmhub==4.7 \
    && pip3 uninstall -y setuptools pip \
    && mkdir -p data \
    && echo 'pragma synchronous = off;' >~/.sqliterc \
    && cd /usr/lib/python3* \
    && python3 -OO -m compileall -q -b -f . \
    && rm -rf site-packages/*.*-info \
    && find . -name __pycache__ | xargs rm -rf \
    && find . -name '*.py' -delete
