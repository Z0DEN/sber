FROM ubuntu:20.04

LABEL maintainer="BlesK maksarestov2000@gmail.com"

ENV GITHUB_LINK https://github.com/Z0DEN/sber.git  

WORKDIR /

COPY ./req.txt /sber/
COPY ./trading.py /sber/
COPY ./supervisor.conf /sber/

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y python3 python3-pip python3-venv git supervisor python3-pyqt5 

RUN cd /sber

RUN pip3 install --upgrade pip
RUN pip3 install -r /sber/req.txt

STOPSIGNAL SIGTERM

CMD supervisord -c /sber/supervisor.conf
