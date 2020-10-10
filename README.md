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

* [OS] - Raspberry Pi OS/Raspbian 9
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
[OS]: <https://www.raspberrypi.org/downloads/>

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
| gunicorn | 20.0.4 |
| requests | 2.21.0 |
| multiprocess | 0.70.10 |

## Architectural diagram

### Bread Board
***Note: The 10k pull up resistor and filtering cap are not shown in this diagram. See the link to the DHT 11 sensor.***

<img src="./images/pitemp_bb.png">

### Schematic

<img src="./images/pitemp_schem.png">

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

## Build a simple broker(mqtt server)
In order to develop and test the PiTemp and the MQTT protocol, you will need to deploy a simple broker to recive the data sent by the PiTemp. The MQTT protocol uses SSL to protect data, and as a best practice should be used in IoT communication channels. The MQTT protocol is used in IoT applications because of it speed and the fault tolerant nature of the protocol.

MQTT - https://mqtt.org/

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

#build a Mosquitto config file
sudo cat /etc/mosquitto/mosquitto.conf <<EOF
pid_file /var/run/mosquitto.pid

persistence true
persistence_location /var/lib/mosquitto/

log_dest file /var/log/mosquitto/mosquitto.log

include_dir /etc/mosquitto/conf.d

#port 8883 is the MQTT secure port
listener 8883
cafile /etc/mosquitto/ca_certificates/ca.crt
keyfile /etc/mosquitto/ca_certificates/server.key
certfile /etc/mosquitto/ca_certificates/server.crt

EOF

#Start Mosquitto broker
sudo mosquitto -d -v -c /etc/mosquitto/mosquitto.conf
```
## Create new certificates
If you need to build a new set of certificates for SSL, use the following script.

```
#!/bin/bash -x
#generate the certificate authority key
openssl genrsa -aes128 -out ca.key -passout pass:mynewpassword 3072

#create a certificate
openssl req -new -passin pass:mynewpassword -x509 -days 2000 -key ca.key -out ca.crt -subj "/C=US/ST=Home/L=HOME/O=Global
Security/OU=MQTT Department/CN=nothing.com"

#generate server keys pairs for the broker
openssl genrsa -out server.key 2048

#create the server csr
openssl req -new -out server.csr -key server.key -subj "/C=US/ST=Home/L=HOME/O=Global Security/OU=MQTT Department/CN=nothi
ng.com"

#create the server cert signed with the ca key
openssl x509 -passin pass:mynewpassword -req -in server.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out server.crt -days
 360
```

## Run PiTemp
### Configure the PiTemp
In order to configure the PiTemp to match your environment edit the settings.py file.
```
#hostname
HOSTNAME = socket.gethostname()

#DHT11 or DHT22
SENSORTYPE = os.getenv('SENSORTYPE',None)

#Celcius or Fahrenheit
SCALE = os.getenv('SCALE',None)

#The GPIO pins to use for sensors
PINS = os.getenv('PINS',None)
#Take comma seperated string and turn into list so it can be used.
PINS = PINS.split(',')

#Time to sleep in seconds
SLEEP = os.getenv('SLEEP',None)

# on the PiOLED this pin isnt used
RST = os.getenv('RST',None)

#The time interval
INTERVAL = os.getenv('INTERVAL',None)

#physical network name wlan0 or eth0
PHYSNET = os.getenv('PHYSNET',None)

#mgtt broker host, IP or URL
MQTTBROKER = os.getenv('MQTTBROKER',None)

#The port used for mqtt, for SSL we need to use port 8883
MQTTPORT = os.getenv('MQTTPORT',None)
MQTTPORT = int(MQTTPORT)

SSLCERTPATH = os.getenv('SSLCERTPATH',None)

SSLCERT = os.getenv('SSLCERT',None)
```

### Start the PiTemp IoT device
```
# python3 pitemp.py
```
### Start the broker(server)
```
# sudo mosquitto -d -v -c /etc/mosquitto/mosquitto.conf
```

---

# Part 3 - How it works 
## Hardware Components
### DHT11
Per elprocus.com, The DHT11 sensor consists of a capacitive humidity sensing element and a thermistor for sensing temperature.  The humidity sensing capacitor has two electrodes with a moisture holding substrate as a dielectric between them. Change in the capacitance value occurs with the change in humidity levels. The IC measure, process this changed resistance values and change them into digital form.

For measuring temperature this sensor uses a Negative Temperature coefficient thermistor, which causes a decrease in its resistance value with increase in temperature. To get larger resistance value even for the smallest change in temperature, this sensor is usually made up of semiconductor ceramics or polymers.

The temperature range of DHT11 is from 0 to 50 degree Celsius with a 2-degree accuracy. Humidity range of this sensor is from 20 to 80% with 5% accuracy. The sampling rate of this sensor is 1Hz .i.e. it gives one reading for every second.  DHT11 is small in size with operating voltage from 3 to 5 volts. The maximum current used while measuring is 2.5mA.

URL - https://www.elprocus.com/a-brief-on-dht11-sensor/

You should use the DHT 11 module since it already has the 10k resistor and filtering capacitor already soldered onto the PCB. This helps to unclutter your breadboard.

Front

<img src="./images/DHT11module-front.jpg">

Back

<img src="./images/DHT11module-back.jpg">

### SSD1306 OLED
The ssd1306 OLED screen is a 128x64 display and is ideal for smal projects. The screen can be easily hooked up to either an Arduino or Raspberry PI using the SPI output on the GPIO. 

URL - https://components101.com/oled-display-ssd1306

### Raspberry PI 3
One of the most popular single board computers which is powerful enough for any hobby project and comes in at a very affordable price point. The main features of the board are 64bit, quad core ARM CPU, 1Gb of ram, 802.11 a/b ethernet, and HDMI video output. The board can be set up very quickly by flashing the Raspberry PI OS to a micro SD card, and powering on the board.

URL - https://www.raspberrypi.org/documentation/hardware/raspberrypi/README.md

## Protocols
### MQTT Protocol

<img src="./images/MQTT-hor.png">

MQTT is a lightweight publish/subscribe messaging protocol designed for M2M (machine to machine) telemetry in low bandwidth environments.

URL - http://mqtt.org

URl - http://www.steves-internet-guide.com/mqtt/

---

# Part 4 - Extra Credit

## Set up thingsboard
```bash
#!/bin/bash -x

#This setup script is based on the in memory setup for a pi3 found on the thingsboard site
#https://thingsboard.io/docs/user-guide/install/rpi/?ubuntuThingsboardQueue=inmemory

#What adapter will Thingsboard use. 
ETH='wlan0'

#If the DB has never been used just leave blank, if exisiting db set password here
export env PSQLPASS=''

#The new password to set
export env NEWPSQLPASS='newpass'

#get the IP of the primary adapter
export env IP=`ip addr | grep $ETH -A2 | grep 'inet' | head -1 | awk '{print $2}' | cut -f1  -d'/'`

#update the OS and install Java
sudo apt update
sudo apt install -y openjdk-8-jdk

#make sure we use open JDK 8 by default
sudo update-alternatives --config java

#Get thingsboard 3.0.1
wget https://github.com/thingsboard/thingsboard/releases/download/v3.0.1/thingsboard-3.0.1.deb

#install thingsboard
sudo dpkg -i thingsboard-3.0.1.deb

#Set up pg sql - can be used for deloyments with less than 5000 devices reporting in
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
RELEASE=$(lsb_release -cs)
echo "deb http://apt.postgresql.org/pub/repos/apt/ ${RELEASE}"-pgdg main | sudo tee  /etc/apt/sources.list.d/pgdg.list
sudo apt update
sudo apt -y install postgresql-11
sudo service postgresql start

#configure postgres
export env PGPASSWORD=${PSQLPASS}
if [ -n $NEWPSQLPASS ]
then
    psql -U postgres -d postgres -h 127.0.0.1 -c "ALTER USER postgres WITH PASSWORD '"${NEWPSQLPASS}"';"
fi
psql -U postgres -d postgres -h 127.0.0.1 -c "CREATE DATABASE thingsboard;"

#thingsboard config
# DB Configuration
(
cat   << 'EOF'
export DATABASE_ENTITIES_TYPE=sql
export DATABASE_TS_TYPE=sql
export SPRING_JPA_DATABASE_PLATFORM=org.hibernate.dialect.PostgreSQLDialect
export SPRING_DRIVER_CLASS_NAME=org.postgresql.Driver
export SPRING_DATASOURCE_URL=jdbc:postgresql://${IP}:5432/thingsboard
export SPRING_DATASOURCE_USERNAME=postgres
export SPRING_DATASOURCE_PASSWORD=${NEWPSQLPASS}
export SPRING_DATASOURCE_MAXIMUM_POOL_SIZE=5
# Specify partitioning size for timestamp key-value storage. Allowed values: DAYS, MONTHS, YEARS, INDEFINITE.
export SQL_POSTGRES_TS_KV_PARTITIONING=MONTHS
export JAVA_OPTS="$JAVA_OPTS -Xms256M -Xmx256M"
EOF
) >> /etc/thingsboard/conf/thingsboard.conf

#load thingsboard
sudo /usr/share/thingsboard/bin/install/install.sh

#start the service
sudo service thingsboard start

while [ out -ne 200 ]
do
    out = curl -o /dev/null -s -w "%{http_code}\n" http://${IP}:8080
    sleep(5)
    echo 'Waiting for Thingsboard to come up'
done

echo 'Thingsboard is up'
echo 'http://${IP}/8080'
```

## Rest API
``` Bash
# Get the system status
curl -i -k -X GET https://192.168.1.56:10500/api/1.0/status

# Check if the system is alive
curl -i -k -X POST https://192.168.1.56:10500/api/1.0/alive

# Get the current config or set new config options.
curl -i -k -X GET https://192.168.1.56:10500/api/1.0/config

curl -i -k -X PATCH https://192.168.1.56:10500/api/1.0/config
```
