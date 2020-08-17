FROM python:3.7-alpine
MAINTAINER george

ENV PYTHONUNBUFFERED 13

COPY ./requirements.txt /requirements.txt

# Install postgres client dependencies
RUN apk add --update --no-cache postgresql-client
RUN apk add --update --no-cache --virtual .tmp-build-deps \
    gcc libc-dev linux-headers postgresql-dev

RUN pip install -r /requirements.txt

# Remove temp dependencies required to install postgres client
RUN apk del .tmp-build-deps

RUN mkdir /app
WORKDIR /app
COPY ./app /app

RUN adduser -D user
USER user