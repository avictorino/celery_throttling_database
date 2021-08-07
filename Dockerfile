FROM python:3.8-slim
RUN mkdir /app
WORKDIR /app
ADD . /app


RUN \
 apt-get update -y -qq && \
 apt-get -y install gcc && \
 pip install --upgrade --quiet pip && \
 pip install -r requirements.txt --quiet && \
 pip install --quiet gunicorn

RUN apt-get clean