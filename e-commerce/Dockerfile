# Dockerfile
FROM python:3.11-alpine

WORKDIR /e-commerce
COPY . /e-commerce
RUN pip install -r requirements.txt

ENTRYPOINT python Seed.py && python Queries.py