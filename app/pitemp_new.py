#!/bin/python
#rpi based temp monitoring and alerting
import time
import datetime
import logging
import Adafruit_DHT
import Adafruit_SSD1306
import settings
import schedule
import multiprocessing

from pitemp_lib import pitemp

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

class pitemp_iot():

    def __init__(self):
        """
        Set up the pitemp IOT output
        """
        self.plib = pitemp()
        #get the pins
        self.PIN = settings.PINS
        self.sensor = Adafruit_DHT.DHT11

        if(settings.SCALE=='Fahrenheit'):
            self.temp_scale = 'F'
        else:
            self.temp_scale = 'C'

        # 128x32 display with hardware I2C:
        #disp = Adafruit_SSD1306.SSD1306_128_64(rst=settings.RST)
        self.disp = Adafruit_SSD1306.SSD1306_128_64(rst=None)

        # Initialize library.
        self.disp.begin()

        # Clear display.
        self.disp.clear()
        self.disp.display()

        self.width = self.disp.width
        self.height = self.disp.height
        self.image = Image.new('1', (self.width, self.height))

        # Get drawing object to draw on image.
        self.draw = ImageDraw.Draw(self.image)

        # Draw a black filled box to clear the image.
        self.draw.rectangle((0,0,self.width,self.height), outline=0, fill=0)

        # Draw some shapes.
        # First define some constants to allow easy resizing of shapes.
        padding = -2
        self.top = padding
        self.bottom = self.height-padding

        # Move left to right keeping track of the current x position for drawing shapes.
        self.x = 0

        # Load default font.
        self.font = ImageFont.load_default()


    def send_system_status(self):
        #send a current status to the mqtt server
        stats = plib.get_system_status()
        try:
            plib.send_status_mqtt(stats)
        except Exception as e:
            logging.warn("Could not connect to the mqtt broker to send system status")

    def send_temp_hume_data_mqtt(self,input_dict):
        # Sent the data via mqtt to the mqtt server
        # send messages to the mqtt broker
        try:
            plib.send_data_mqtt({"sensor":"sensor"+pin,"temp":temperature,"humidity":humidity,"scale":temp_scale})
        except Exception as e:
            logging.warn("Could not connect to the mqtt broker to send sensor data.")

    def send_temp_hume_data_db(self,input_dict):
        # Sent the data to the db to be held for 72 hours
        try:
            plib.db_insert({"sensor":"sensor"+pin,"temp":temperature,"humidity":humidity,"scale":temp_scale})
        except Exception as e:
            logging.warn("Could not connect to the mqtt broker,writing to internal datastore")

    def display_header(self):
        while True:
            #The header format
            header = "{0:<10}{1:<4}{2:<4}{3:<4}"
            temp_output = "{0:<10}"
            hume_out = "{0:<10}"

            # Draw a black filled box to clear the image.
            ip_addr = self.plib.get_nic_ip_info(settings.PHYSNET)
            dt = datetime.datetime.now()
            self.draw.rectangle((0,0,self.width,self.height), outline=0, fill=0)
            self.draw.text((self.x, self.top),"Time: "+dt.strftime('%H:%M:%S'), font=self.font, fill=255)
            self.draw.text((self.x, self.top+8),"IP: "+ip_addr['ip'], font=self.font, fill=255)
            self.draw.text((self.x, self.top+16)," ", font=self.font, fill=255)
            self.draw.text((self.x, self.top+25),header.format("Sensor: ",1,2,3), font=self.font, fill=255)
            self.draw.text((self.x, self.top+33),"---------------------", font=self.font, fill=255)

            self.draw.text((self.x, top+41),temp_output.format("Temp "+output['temp_scale']+":", font=font, fill=255)
            self.draw.text((self.x, top+49),humid_out.format("Humidity: ", font=font, fill=255)

            # Display image.
            self.disp.image(self.image)
            self.disp.display()

    def display_data(self,pin):
        """
        Set up the display and output to it
        """

        while True:
            #lets print the output of the sensors
            output = {}
            try:
                humidity, temperature = Adafruit_DHT.read_retry(self.sensor, pin)
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

            #send data to the MQTT broker
            self.send_temp_hume_data_mqtt(output)

            #send data to onboard db
            self.send_temp_hume_data_db(output)

            temp_output = "{0:<10}{1:<4}{2:<4}{3:<4}"
            humid_out = "{0:<10}{1:<4}{2:<4}{3:<4}"

            self.draw.text((self.x, top+41),temp_output.format("Temp "+output['temp_scale']+":",int(output['temp_pin%s'%(str(PIN[0]))]), int(output['temp_pin%s'%(str(PIN[1]))]),int(output['temp_pin%s'%(str(PIN[2]))])), font=font, fill=255)
            self.draw.text((self.x, top+49),humid_out.format("Humidity: ",int(output['humidity_pin%s'%(str(PIN[0]))]),int(output['humidity_pin%s'%(str(PIN[1]))]),int(output['humidity_pin%s'%(str(PIN[2]))])) , font=font, fill=255)

            # Display image.
            self.disp.image(self.image)
            self.disp.display()

def main():
    yo = pitemp_iot()

    proc_01 = multiprocessing.Process(target = yo.display_header)
    proc_01.start()

    procs = [multiprocessing.Process(target = yo.display_data, args=(pin,)) for pin in settings.PINS]
    for p in procs:
        p.start()

    proc_01.join()

    for p in procs:
        p.join()

if __name__=='__main__':
    #Run the function
    main()
    #schedule.every(settings.INTERVAL).seconds.do(main())