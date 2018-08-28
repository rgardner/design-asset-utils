FROM python:3.7
ENV PYTHONUNBUFFERED 1

RUN apt-get update --yes && apt-get install --yes chromium chromedriver

RUN set -ex && mkdir /app
WORKDIR /app

ADD Pipfile /app
ADD Pipfile.lock /app
RUN set -ex && pip install pipenv --upgrade
RUN set -ex && pipenv install --dev --system --ignore-pipfile --deploy

ADD . /app
