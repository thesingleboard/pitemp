FROM python:3.8.2-slim-buster
MAINTAINER Jonathan Arrance <jonathan@dragonfleye.io>

ENV INSTALL_PATH /opt/pitemp

RUN apt-get update -y;apt-get install -y curl

RUN mkdir -p $INSTALL_PATH

WORKDIR $INSTALL_PATH

RUN pip3 install --upgrade pip
ADD requirements.txt /
RUN pip3 install -r /requirements.txt
#sudo apt install software-properties-common

