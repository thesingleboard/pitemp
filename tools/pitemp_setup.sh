#!/bin/bash
sudo apt-get -y update
sudo apt-get upgrade

sudo apt-get install -y python3-pip
sudo apt install -y python3-dev
sudo apt install -y python-imaging python-smbus i2c-tools
sudo apt install -y python3-pil
sudo apt install -y python3-setuptools
#sudo apt install -y python3-rpi.gpio

sudo pip3 install --upgrade setuptools

sudo `echo 'dtoverlay=spi1-3cs' `>> /boot/config.txt

sudo pip3 install RPI.GPIO
sudo pip3 install adafruit-blinka
sudo pip3 install adafruit-circuitpython-dht
sudo pip3 install schedule
sudo pip3 install pysqlite3

sudo apt install -y python-smbus
sudo apt-get install -y libgpiod2
sudo apt install -y i2c-tools

