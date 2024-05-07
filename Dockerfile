FROM mcr.microsoft.com/windows-cssc/python:3.11-nanoserver-ltsc2019

WORKDIR /app
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY ./ ./