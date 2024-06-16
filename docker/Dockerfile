FROM python:3.11-bookworm

RUN apt update && apt install -y build-essential

RUN mkdir /app
COPY . /app
COPY docker/config.yaml /app/config.yaml

WORKDIR /app
ENTRYPOINT python3 WebHost.py
