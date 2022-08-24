# syntax=docker/dockerfile:1

FROM python:3.10.6-slim-bullseye

WORKDIR /code

COPY requirements.txt requirements.txt
RUN apt-get update
RUN apt-get install -y python3-pip python3-dev cmake libssl-dev libffi-dev ffmpeg libsm6 libxext6
RUN pip3 install -r requirements.txt
RUN pip3 install gunicorn

