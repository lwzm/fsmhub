FROM python:3.7-slim-stretch

LABEL maintainer="lwzm@qq.com"
ARG bjoern=bjoern-3.0.1-cp37-cp37m-linux_x86_64.whl

WORKDIR /home/

COPY libev.so.4 /usr/lib/x86_64-linux-gnu/libev.so.4
COPY $bjoern ./
RUN pip install --no-cache-dir fsm-hub psycopg2-binary redis $bjoern \
    && rm -f $bjoern \
    && find /usr/local/lib/ -name '*.pyc' -delete

ENV REDIS ""
EXPOSE 1024
CMD [ "fsm-hub" ]
