FROM python:3.9.5-slim-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /manage_products

RUN pip install --upgrade pip

COPY requirements.txt /manage_products/

RUN pip install -r requirements.txt

COPY . /manage_products/
