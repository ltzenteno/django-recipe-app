FROM python:3.7-alpine
MAINTAINER Luis Zenteno

# it is recommended to run python unbuffered within docker containers
ENV PYTHONUNBUFFERED 1

# install dependencies
COPY ./requirements.txt /requirements.txt

# install PostgreSQL client
RUN apk add --update --no-cache postgresql-client

# required for Pillow package
RUN apk add --update --no-cache jpeg-dev

# install dependencies needed by postgres and Pillow (musl-dev zlib zlib-dev)
RUN apk add --update --no-cache --virtual .tmp-build-deps \
        gcc libc-dev linux-headers postgresql-dev musl-dev zlib zlib-dev

RUN pip install -r /requirements.txt

# delete temporary requirements for postgres
RUN apk del .tmp-build-deps

RUN mkdir /app
WORKDIR /app
COPY ./app /app

# create dir to store user uploaded images
RUN mkdir -p /vol/web/media

RUN mkdir -p /vol/web/static

# creating a user to run our project inside the alpine container
RUN adduser -D user

# sets ownership of all dirs inside vol dir to our custom user
RUN chown -R user:user /vol/

RUN chmod -R 755 /vol/web

USER user