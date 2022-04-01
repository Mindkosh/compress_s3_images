FROM jfloff/alpine-python:latest-slim

RUN apk update

RUN apk add --virtual build-deps gcc python3-dev musl-dev && \
    apk add jpeg-dev zlib-dev libjpeg && \
    pip install Pillow && \
    apk del build-deps

RUN pip install boto3