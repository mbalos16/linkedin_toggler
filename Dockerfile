FROM python:3.9.2-alpine

# Install linux dependencies
RUN apk add firefox
RUN apk add bash

# Install CRON
RUN apk add busybox-initscripts

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

# Configure crontab
COPY configure_crontabs.sh configure_crontabs.sh
RUN bash configure_crontabs.sh

# Copy project files
COPY logging.ini logging.ini
COPY main.py main.py
COPY secrets.json secrets.json

# Default executable when running the container
ENTRYPOINT crond && bash
