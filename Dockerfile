# Dockerfile

FROM python:3.10.8-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    apt-get install -y libpq-dev gcc

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .