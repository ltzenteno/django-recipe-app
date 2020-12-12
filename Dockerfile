FROM python:3.7-alpine
MAINTAINER Luis Zenteno

# it is recommended to run python unbuffered within docker containers
ENV PYTHONUNBUFFERED 1

# install dependencies
COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

RUN mkdir /app
WORKDIR /app
COPY ./app /app

# creating a user to run our project inside the alpine container
RUN adduser -D user
USER user