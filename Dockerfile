#!/usr/bin/env bash
# Build metmini actuald container
# i.e. the Daemon that collects met data and stores in Database
# Can something smaller be built from Alpine or a Python Docker image ?
# https://stackoverflow.com/questions/46503947/how-to-get-pipenv-running-in-docker

FROM registry:5000/gold-centos7:1.0.0
LABEL author="Richard Crouch"
LABEL description="MetMini ActualD container"

# FIXME : pipenv complains if not here - can this be added to gold-centos ?
ENV LC_ALL=en_US.utf-8
ENV LANG=en_US.utf-8

# Install pyenv - https://gist.github.com/jprjr/7667947
# =====================================================
# Dependencies for installing pyenv
RUN yum -y install git zlib-devel gcc openssl-devel bzip2-devel libffi-devel make
RUN useradd -m python_user
WORKDIR /home/python_user
USER python_user
RUN git clone git://github.com/yyuu/pyenv.git .pyenv
ENV HOME  /home/python_user
ENV PYENV_ROOT $HOME/.pyenv
ENV PATH $PYENV_ROOT/shims:$PYENV_ROOT/bin:$PATH
RUN pyenv install -v 3.8.5
RUN pyenv global 3.8.5
RUN pyenv rehash

# RUN yum install -y python3 python3-devel python3-pip
#RUN yum install -y python3-devel

USER root
# Needed for mariadb-connector-c
RUN yum install -y http://repo.okay.com.mx/centos/7/x86_64/release/okay-release-1-1.noarch.rpm
RUN yum install -y mariadb-libs
RUN yum install -y mariadb-devel
RUN yum install -y mariadb-connector-c

# Debugging
RUN yum install -y nmap

# Copy application and files
RUN mkdir /app
COPY app/*.py /app/
COPY etc/entrypoint.sh /etc
RUN ["chmod", "+x", "/etc/entrypoint.sh"]

USER python_user
# Install Python dependencies
RUN pip3 install pipenv
COPY Pipfile* ./
RUN pipenv install --system --deploy

WORKDIR /app

ENTRYPOINT ["/etc/entrypoint.sh"]
