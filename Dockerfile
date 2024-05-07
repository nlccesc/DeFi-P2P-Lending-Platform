FROM python:3.12-alpine

# TODO: Fix pip installation not working

WORKDIR /app
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY ./ ./