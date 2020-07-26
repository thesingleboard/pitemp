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

## Python library version
rpi.gpio = 0.7.0
jinja2 = 2.10.1
adafruit-blinka = 4.2.0
adafruit-circuitpython-dht = 3.4.0
schedule = 0.6.0
adafruit-ssd1306 = 1.6.2
adafruit-dht = 1.4.0
adafruit-platformdetect = 2.5.0
adafruit-pureio = 1.0.4
flask = 1.0.0
paho-mqtt = 1.5.0

## Architectural diagram

## Assemble the prototype
---

# Part 2 - Build the PiTemp
## Programming the hardware

## Build a simple broker

## Set up your pitemp

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
