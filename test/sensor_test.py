#!/bin/python
#rpi based temp monitoring and alerting
import time
import multiprocessing
import subprocess
import Adafruit_DHT
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
import settings

def temp_sensor():
    #get the sensor
    #sensor = 'Adafruit_DHT.'+settings.SENSORTYPE
    sensor = Adafruit_DHT.DHT11
    #Pins where DHT11 sensors connected
    pins = settings.PINS
    print(pins)

    #lets print the output of the sensors
    output = {}
    for pin in pins:
        print(pin)
        try:
            humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
            print(temperature)
            temp_scale = 'C'
            if(settings.SCALE == 'Fahrenheit'):
                temperature = temperature * 9/5.0 + 32
                temp_scale = 'F'
            output['temp_pin%s_%s'%(pin,temp_scale)] = temperature
            output['humidity_pin%s'%(pin)] = humidity
            #print( "Temp: {:.1f} {} Humidity: {}% ".format(temperature, temp_scale, humidity))
        except RuntimeError as error:
            print(error.args[0])
    print(output)
    return output

if __name__=='__main__':

    while True:
        #get the temp from the sensors
        temp = temp_sensor()
        print(temp)

        #if there is an overheat situation blink the led
        #screen(temp)
    
        
        time.sleep(.1)
