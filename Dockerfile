FROM python:3.7-alpine
MAINTAINER Luis Zenteno

# it is recommended to run python unbuffered within docker containers
ENV PYTHONUNBUFFERED 1

# install dependencies
COPY ./requirements.txt /requirements.txt

# install PostgreSQL client
RUN apk add --update --no-cache postgresql-client

# install dependencies needed by postgres
RUN apk add --update --no-cache --virtual .tmp-build-deps \
        gcc libc-dev linux-headers postgresql-dev

RUN pip install -r /requirements.txt

# delete temporary requirements for postgres
RUN apk del .tmp-build-deps

RUN mkdir /app
WORKDIR /app
COPY ./app /app

# creating a user to run our project inside the alpine container
RUN adduser -D user
USER user