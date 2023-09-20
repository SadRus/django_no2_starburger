FROM python:3.8.3-alpine

WORKDIR /usr/src/starburger

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add postgresql-dev \
    && apk add jpeg-dev zlib-dev libjpeg

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt \
    && apk del build-deps

COPY . .

