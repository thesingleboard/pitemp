#!/bin/python
import os
import socket
import time
import calendar

#api version
API = os.getenv('API',None)

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

MQTTPORT = os.getenv('MQTTPORT',None)
MQTTPORT = int(MQTTPORT)

SSLCERTPATH = os.getenv('SSLCERTPATH',None)

SSLCERT = os.getenv('SSLCERT',None)

#defaults to one hour interval
STATUSINTERVAL = os.getenv('STATUSINTERVAL',3600)

#get the epoc time 
STARTOFTIME = calendar.timegm(time.gmtime())

#DC = 23
#SPI_PORT = 0
#SPI_DEVICE = 0

CONFIG = {  'API':API,
            'HOSTNAME':HOSTNAME,
            'SENSORTYPE':SENSORTYPE,
            'SCALE':SCALE,
            'PINS':PINS,
            'SLEEP':SLEEP,
            'RST':RST,
            'INTERVAL':INTERVAL,
            'PHYSNET':PHYSNET,
            'MQTTBROKER':MQTTBROKER,
            'MQTTPORT':MQTTPORT,
            'SSLCERTPATH':SSLCERTPATH,
            'SSLCERT':SSLCERT,
            'STATUSINTERVAL':STATUSINTERVAL,
            'STARTOFTIME':STARTOFTIME
            }