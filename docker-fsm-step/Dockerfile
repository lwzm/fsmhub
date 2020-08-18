FROM python:slim

LABEL maintainer="lwzm@qq.com"

ENTRYPOINT [ "fsm-step" ]
ENV LOGURU_LEVEL="INFO" SENTRY="" FSMHUB=""
RUN pip3 install --no-cache-dir loguru sentry-sdk

COPY fsm-step /bin/
