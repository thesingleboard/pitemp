# PiTemp 
A Raspberry Pi 3 based temperature, humidity and alerting system. Pitemp uses multiple DHT11 sensors to take readings and sends metrics back to a broker using the MQtt protocol. PiTemp is a work in progress and is completly open source. Please feel free to use the code and architecture to build your own projects.

---

# Part 1 - Overview
## Hardware components needed
If you are a hobbiest you may have all of the parts needed to build out the PiTemp. 
* [RaspberryPI3] - The brains of the operation!
* [DHT11] - Sensors used to sample the temperature and humidity.
* [SSD1306] - Small OLED display used to output data.
* [BreadBoard] - Prototyping base used to build the piTemp for development.

[RaspberryPI3]: <https://www.raspberrypi.org/products/raspberry-pi-3-model-b/>
[DHT11]: <https://components101.com/dht11-temperature-sensor>
[SSD1306]: <https://components101.com/oled-display-ssd1306>
[BreadBoard]: <https://en.wikipedia.org/wiki/Breadboard>

## Software Libraries needed
All of the codeing for PiTemp is done using Python3. The reason I chose Python to build PiTemp is because it is easy to understand and can be picked up easily. It isalso one of the mpost popular programming langauges around, and can be used to build everything from simple scripts to machine learning alrorythems.

* [Python3] - The base language used in PiTemp.
* [AdafruitDHT] - An open source DHT11 control library.
* [AdafruitSSD1306] - An open source OLED control library.
* [PahoMqtt] - The Pyhton MQTT library used to send data.
* [Sqlite3] - A simple database used to store metrics.
* [Schedule] - The Python time scheduling library.
* [PIL] - Python imaging library.
* [RpiGPIO] - Python class to control Rpi GPIO interface.
* [jinja2] - Expressive template libraryBlinka.
* [Blinka] - Adafruit Blinka provides a programming interface for Rpi microcontroller.
* [PlatformDetect] - Adafruit best guess platform detection library
* [Pureio] - Pure Python access to SPI and I2C

[Python3]: <https://www.python.org/>
[AdafruitDHT]: <https://github.com/adafruit/Adafruit_Python_DHT>
[AdafruitSSD1306]: <https://github.com/adafruit/Adafruit_SSD1306>
[PahoMqtt]: <https://www.eclipse.org/paho/>
[Sqlite3]: <https://docs.python.org/3/library/sqlite3.html>
[Schedule]: <https://pypi.org/project/schedule/>
[PIL]: <https://www.pythonware.com/products/pil/>
[RpiGPIO]: <https://pypi.org/project/RPi.GPIO/>
[jinja2]: <https://pypi.org/project/Jinja2/>
[Blinka]: <https://pypi.org/project/Adafruit-Blinka/>
[PlatformDetect]: <https://pypi.org/project/Adafruit-PlatformDetect/>
[Pureio]: <https://github.com/adafruit/Adafruit_Python_PureIO/tree/1.0.4>

## Python library version
|  Library | Version  |
| ------------ | ------------ |
|  rpi.gpio |  0.7.0 |
|  jinja2 | 2.10.1  |
|  adafruit-blinka |  4.2.0 |
|  schedule | 0.6.0  |
| adafruit-ssd1306  | 1.6.2  |
| adafruit-dht | 1.4.0 |
| adafruit-platformdetect | 2.5.0 |
| adafruit-pureio | 1.0.4 |
| paho-mqtt | 1.5.0 |

## Architectural diagram

## Assemble the prototype
---

# Part 2 - Build the PiTemp
## Set up the PiTemp
The following bash script will install everything needed to develop and run the PiTemp code.

```bash
#!/bin/bash
#make sure you have the certificate before setting up.

#The certificate needed to connect to the broker.
#In this project we will generate the certificates on our example broker.
CERT='ca.crt'
CERTPATH='~/pitemp/certs'

#Update the underlying libraries.
sudo apt-get -y update
sudo apt-get upgrade

#Install all of the Python 3 components
sudo apt-get install -y python3-pip
sudo apt install -y python3-dev
sudo apt install -y python-imaging python-smbus i2c-tools
sudo apt install -y python3-pil
sudo apt install -y python3-setuptools

#Upgrade the setup tools
sudo pip3 install --upgrade setuptools

#Enable SPI on the RPi
sudo `echo 'dtoverlay=spi1-3cs' `>> /boot/config.txt

#Install the needed Python3 libraries
sudo pip3 install RPI.GPIO
sudo pip3 install adafruit-blinka
sudo pip3 install adafruit-circuitpython-dht
sudo pip3 install schedule
sudo pip3 install pysqlite3

sudo apt install -y python-smbus
sudo apt-get install -y libgpiod2
sudo apt install -y i2c-tools

#copy the ca.crt file to the correct location
sudo mkdir -p ${CERTPATH}
sudo cp ${CERT} ${CERTPATH}
```

## Programming the hardware

## Build a simple broker
```
#!/bin/bash

sudo apt update
sudo apt install -y mosquitto mosquitto-clients
sudo systemctl enable mosquitto.service

#configure the ca certs
#NOTE: This is on raspbian
#generate the certificate authority key
sudo openssl genrsa -aes128 -out ca.key -passout pass:mynewpassword 3072

#create a certificate
sudo openssl req -new -passin pass:mynewpassword -x509 -days 2000 -key ca.key -out ca.crt -subj "/C=US/ST=Home/L=HOME/O=Global Security/OU=MQTT Department/CN=nothing.com"

#generate server keys pairs for the broker
sudo openssl genrsa -out server.key 2048

#create the server csr
sudo openssl req -new -out server.csr -key server.key -subj "/C=US/ST=Home/L=HOME/O=Global Security/OU=MQTT Department/CN=nothing.com"

#create the server cert signed with the ca key
sudo openssl x509 -passin pass:mynewpassword -req -in server.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out server.crt -days 360

#Copy the certs to the proper location on the broker
sudo cp ca.crt /etc/mosquitto/ca_certificates/
sudo cp server.crt /etc/mosquitto/ca_certificates/
sudo cp server.key /etc/mosquitto/ca_certificates/

#copy the client certs to a client folder
sudo mkdir client_cert
sudo cp ca.crt ./client_cert

#Configure the broker
sudo mv /etc/mosquitto/mosquitto.conf /etc/mosquitto/mosquitto.old

sudo cat /etc/mosquitto/mosquitto.conf <<EOF
pid_file /var/run/mosquitto.pid

persistence true
persistence_location /var/lib/mosquitto/

log_dest file /var/log/mosquitto/mosquitto.log

include_dir /etc/mosquitto/conf.d

listener 8883
cafile /etc/mosquitto/ca_certificates/ca.crt
keyfile /etc/mosquitto/ca_certificates/server.key
certfile /etc/mosquitto/ca_certificates/server.crt

EOF

sudo mosquitto -d -v -c /etc/mosquitto/mosquitto.conf
```

## Run PiTemp
---

# Part 3 - How it works 
## Hardware Components
### DHT11
### LCD screen output
### MQTT

## MQTT Protocol

## DHT11 Sensor
---

# Part 4 - Extra Credit
## Set up thingsboard

## Build a rest API

## Simple Graphing Web Service
