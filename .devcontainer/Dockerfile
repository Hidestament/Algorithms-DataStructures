FROM python:3.10-slim

WORKDIR /app

RUN apt-get update
RUN apt-get install -y git

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
