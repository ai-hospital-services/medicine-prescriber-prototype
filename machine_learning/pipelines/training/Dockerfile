FROM --platform=linux/amd64 python:3.9.14-slim-buster

WORKDIR /
COPY requirements.txt .

RUN apt-get update && apt-get upgrade -y && \
    pip install --upgrade pip && \
    pip install --no-cache-dir -r ./requirements.txt
