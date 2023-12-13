# Dockerfile
FROM python:3.11-alpine

WORKDIR /e-commerce
COPY . /e-commerce
COPY requirements.txt /e-commerce/requirements.txt
RUN pip install -r requirements.txt

RUN apk update && apk add npm

RUN npm install react-bootstrap bootstrap