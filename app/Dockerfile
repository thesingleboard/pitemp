FROM python:3.8.2-slim-buster
MAINTAINER Jonathan Arrance <jonathan@dragonfleye.io>

ENV INSTALL_PATH /opt/pitemp

RUN apt-get update -y;apt-get install -y curl;apt-get install -y python3-pip;apt install -y python3-dev;apt install -y python-imaging; apt install -y python-smbus;apt install -y i2c-tools; \
apt install -y python3-pil;apt install -y python3-setuptools;apt install -y python-smbus;apt-get install -y libgpiod2;apt install -y i2c-tools;apt install -y python3-openssl

RUN mkdir -p $INSTALL_PATH

WORKDIR $INSTALL_PATH

RUN pip3 install --upgrade pip
ADD requirements.txt /
RUN pip3 install -r /requirements.txt
#sudo apt install software-properties-common

ADD pitemp.py $INSTALL_PATH
ADD pitemp_lib.py $INSTALL_PATH
ADD settings.py $INSTALL_PATH

EXPOSE 8883

#CMD ["python3","pitemp.py"]
