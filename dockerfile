# syntax=docker/dockerfile:1

FROM python:3.11-rc-alpine3.16

WORKDIR /code

COPY requirements.txt requirements.txt
RUN apk add --no-cache postgresql-libs && \
    apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev
RUN python3 -m pip install -r requirements.txt
RUN apk --purge del .build-deps 
RUN pip3 install gunicorn

