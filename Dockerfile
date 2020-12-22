#!/usr/bin/env bash
# Build metmini actuald container
# i.e. the Daemon that collects met data and stores in Database

FROM registry:5000/gold-centos7:1.0.0
LABEL author="Richard Crouch"
LABEL description="MetMini ActualD container"

# Needed for mariadb-connector-c
RUN yum install -y http://repo.okay.com.mx/centos/7/x86_64/release/okay-release-1-1.noarch.rpm
RUN yum install -y python3 python3-devel
RUN yum install -y mariadb-libs
RUN yum install -y mariadb-devel
RUN yum install -y mariadb-connector-c

# Debugging
RUN yum install -y nmap

# Prerequisites
COPY requirements.txt /tmp
RUN pip3 install -r /tmp/requirements.txt

# Copy application and files
RUN mkdir /app
COPY app/*.py /app/

COPY etc/entrypoint.sh /etc
RUN ["chmod", "+x", "/etc/entrypoint.sh"]

WORKDIR /app

ENTRYPOINT ["/etc/entrypoint.sh"]
