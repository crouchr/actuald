#!/usr/bin/env bash
# Build metmini actuald container
# i.e. the Daemon that collects met data and stores in Database
# Can something smaller be built from Alpine or a Python Docker image ?
# https://stackoverflow.com/questions/46503947/how-to-get-pipenv-running-in-docker

FROM centos/python-38-centos7
LABEL author="Richard Crouch"
LABEL description="MetMini ActualD container"

# FIXME : pipenv complains if not here - can this be added to gold-centos ?
ENV LC_ALL=en_US.utf-8
ENV LANG=en_US.utf-8

# generate logs in unbuffered mode
ENV PYTHONUNBUFFERED=1

USER root

# Copy application and files
RUN mkdir /app
COPY app/*.py /app/

# Install Python dependencies
RUN pip3 install pipenv
COPY Pipfile* ./
RUN pipenv install --system --deploy --verbose

WORKDIR /app

# run Python unbuffered so the logs are flushed
CMD ["python3", "-u", "actuald.py"]
#CMD ["tail", "-f", "/dev/null"]
