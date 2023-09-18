FROM ubuntu:20.04 AS builder

LABEL maintainer="BlesK maksarestov2000@gmail.com"

ENV GITHUB_LINK https://github.com/Z0DEN/sber.git  

WORKDIR /

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y python3 python-pip python-virtualenv git

RUN git clone $GITHUB_LINK && \
    cd /sber

RUN python -m venv ./pyton-venv && \
    source ./python-venv/bin/activate

RUN pip3 install --upgrade pip
RUN pip3 install -r ./req.txt

STOPSIGNAL SIGTERM

CMD python3 trading.py
