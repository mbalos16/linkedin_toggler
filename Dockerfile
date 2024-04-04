FROM python:3.9.2-alpine

# Install linux dependencies
RUN apk add firefox
RUN apk add bash

# Set date and timezone
RUN apk add -U tzdata
ENV TZ=Europe/London
RUN cp /usr/share/zoneinfo/Europe/London /etc/localtime

# Set working directory 
RUN mkdir /app
WORKDIR /app

# Install python libraries
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy project files
COPY logging.ini logging.ini
COPY main.py main.py
COPY secrets.json secrets.json

# Default executable when running the container
ENTRYPOINT bash