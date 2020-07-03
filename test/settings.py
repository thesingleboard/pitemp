#!/bin/python
#DHT11 or DHT22
SENSORTYPE='DHT11'

#Celcius or Fahrenheit
SCALE='Fahrenheit'

#The GPIO pins to use for sensors
PINS = ['24','23','4']

#Time to sleep in seconds
SLEEP = 2

# on the PiOLED this pin isnt used
RST = None

DC = 23
SPI_PORT = 0
SPI_DEVICE = 0