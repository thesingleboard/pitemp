#!/bin/python
#rpi based temp monitoring and alerting
import time
import datetime
#import multiprocessing
#import subprocess
import Adafruit_DHT
#import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
import settings
import schedule
from pitemp_lib import pitemp

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

def main():
    
    plib = pitemp()
    
    #get the pins
    PIN = settings.PINS
    sensor = Adafruit_DHT.DHT11
    ip_addr = plib.get_nic_ip_info(settings.PHYSNET)
    
    if(settings.SCALE=='Fahrenheit'):
        temp_scale = 'F'
    else:
        temp_scale = 'C'
    
    # 128x32 display with hardware I2C:
    #disp = Adafruit_SSD1306.SSD1306_128_64(rst=settings.RST)
    disp = Adafruit_SSD1306.SSD1306_128_64(rst=None)

    # Initialize library.
    disp.begin()

    # Clear display.
    disp.clear()
    disp.display()

    width = disp.width
    height = disp.height
    image = Image.new('1', (width, height))

    # Get drawing object to draw on image.
    draw = ImageDraw.Draw(image)

    # Draw a black filled box to clear the image.
    draw.rectangle((0,0,width,height), outline=0, fill=0)

    # Draw some shapes.
    # First define some constants to allow easy resizing of shapes.
    padding = -2
    top = padding
    bottom = height-padding
    # Move left to right keeping track of the current x position for drawing shapes.
    x = 0

    # Load default font.
    font = ImageFont.load_default()

    while True:
        #lets print the output of the sensors
        output = {}
        for pin in PIN:
            try:
                humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
                temp_scale = 'C'
                if(settings.SCALE == 'Fahrenheit'):
                    temp_scale = 'F'
                    try:
                        temperature = temperature * 9/5.0 + 32
                    except Exception as e:
                        logging.error('Fahrenheit converison error: %s'%e)
                        temperature=0
                output['temp_pin%s'%(pin)] = temperature
                output['temp_scale'] = temp_scale
                output['humidity_pin%s'%(pin)] = humidity
            except RuntimeError as error:
                print(error.args[0])

            #send messages to the mqtt broker
            try:
                plib.send_mqtt({"sensor":"sensor"+pin,"temp":temperature,"humidity":humidity,"scale":temp_scale})
            except Exception as e:
                logging.warn("Could not connect to the mqtt broker,writing to internal datastore")
            
            plib.db_insert({"sensor":"sensor"+pin,"temp":temperature,"humidity":humidity,"scale":temp_scale})

            #TEST#
            #print(output)
            #####

        dt = datetime.datetime.now()

        #screen string formatting
        header = "{0:<10}{1:<4}{2:<4}{3:<4}"
        temp_output = "{0:<10}{1:<4}{2:<4}{3:<4}"
        humid_out = "{0:<10}{1:<4}{2:<4}{3:<4}"

        # Draw a black filled box to clear the image.
        draw.rectangle((0,0,width,height), outline=0, fill=0)
        draw.text((x, top),"Time: "+dt.strftime('%H:%M:%S'), font=font, fill=255)
        draw.text((x, top+8),"IP: "+ip_addr['ip'], font=font, fill=255)
        draw.text((x, top+16)," ", font=font, fill=255)
        draw.text((x, top+25),header.format("Sensor: ",1,2,3), font=font, fill=255)
        draw.text((x, top+33),"---------------------", font=font, fill=255)
        draw.text((x, top+41),temp_output.format("Temp "+output['temp_scale']+":",int(output['temp_pin%s'%(str(PIN[0]))]), int(output['temp_pin%s'%(str(PIN[1]))]),int(output['temp_pin%s'%(str(PIN[2]))])), font=font, fill=255)
        draw.text((x, top+49),humid_out.format("Humidity: ",int(output['humidity_pin%s'%(str(PIN[0]))]),int(output['humidity_pin%s'%(str(PIN[1]))]),int(output['humidity_pin%s'%(str(PIN[2]))])) , font=font, fill=255)
        
        # Display image.
        disp.image(image)
        disp.display()

if __name__=='__main__':
    #Run the function
    schedule.every(settings.INTERVAL).seconds.do(main())
