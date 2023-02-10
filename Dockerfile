FROM python:3.8.5-slim-buster
WORKDIR /opt
RUN apt-get update  --allow-releaseinfo-change
RUN apt-get update && apt-get install -y --no-install-recommends \
    unixodbc-dev \
    unixodbc \
    libpq-dev
RUN mkdir -p /usr/share/man/man1
RUN  apt-get update --allow-releaseinfo-change && apt-get install -y --no-install-recommends unzip libc6-dev libssl-dev netcat gcc python-pycurl libcurl4-openssl-dev build-essential   default-libmysqlclient-dev
COPY . /opt/indent/
WORKDIR /opt/indent
RUN python -m pip install -r requirements_new.txt