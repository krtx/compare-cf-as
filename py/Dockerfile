FROM python:3.7-slim

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y sysstat && \
    pip install pipenv

WORKDIR /app

COPY Pipfile Pipfile.lock /app/

RUN pipenv install --system

COPY . /app

ENTRYPOINT ["python", "/app/src/main.py"]