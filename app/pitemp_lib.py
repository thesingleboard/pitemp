#lib file for pitemp
import subprocess
import datetime
import settings
import logging
import ssl
import sqlite3
import psutil
import paho.mqtt.client as paho

class pitemp():

    def __init__(self):
        #connect to the mqtt broker
        self.client = paho.Client()
        self.client.tls_set(settings.SSLCERTPATH+"/"+settings.SSLCERT,tls_version=ssl.PROTOCOL_TLSv1_2)
        self.client.tls_insecure_set(True)

        try:
            #connect to the sqlite process
            self.sqlcon = sqlite3.connect('iotdb_%s.db'%(datetime.datetime.now().timestamp()))
            self.cursor = self.sqlcon.cursor()
            self.cursor.execute('''CREATE TABLE mqtt (temp float, humidity float, scale text, sensor text, date text)''')
        except Exception as e:
            logging.warn(e)
            logging.warn("Could not connect to the sqlite DB.")

        try:
            self.client.connect(settings.MQTTBROKER, settings.MQTTPORT, 60)
            self.client.loop_start()
        except Exception as e:
            logging.error(e)
            logging.error("Could not connect to the MQTT Broker")

    def list_nics(self):
        """
        DESC: List the available nics
        INPUT: None
        OUTPUT: out_array - list of nics
        DESC: None
        """
        out_array = []
        try:
            proc = subprocess.Popen("sudo ls -I br* -I lo -I vir* /sys/class/net/", stdout=subprocess.PIPE, shell=True)
            (output,err) = proc.communicate()
            out_array = str(output).strip().split()
        except Exception as e:
            logging.error(e)
            logging.error("Could not get the list of nics")

        return out_array

    def get_nic_ip_info(self,nic):
        """
        DESC: Get the IP of the primary nic
        INPUT: nic - the name of the primary nic
        OUTPUT out_dict - ip
                                      - gateway
        NOTES: None
        """
        try:
            proc = subprocess.Popen("ip addr | grep '%s' -A2 | grep 'inet' | head -1 | awk '{print $2}' | cut -f1  -d'/'"%nic, stdout=subprocess.PIPE, shell=True)
            (output,err) = proc.communicate()
            ip = str(output.decode('ascii').strip())
        except Exception as e:
            ip = e

        try:
            proc2 = subprocess.Popen("/sbin/ip route | awk '/default/ { print $3 }'", stdout=subprocess.PIPE, shell=True)
            (output2,err2) = proc2.communicate()
            gateway = str(output2.decode('ascii').strip())
        except Exception as e:
            gateway = e

        return {'ip':ip,'gateway':gateway}

    def get_cpu_id(self):
        """
        DESC: Get the CPU ID and use it as the unchangebale device id.
        INPUT: None
        OUTPUT: device_id
        """
        # Extract serial from cpuinfo file
        device_id = "0000000000000000"
        try:
            f = open('/proc/cpuinfo','r')
            for line in f:
                if line[0:6]=='Serial':
                    device_id = line[10:26]
            f.close()
        except:
            device_id = "ERROR000000000"
        
        return device_id
    
    def get_uptime(self):
        """
        DESC: Run get system uptime
        INPUT: None
        OUTPUT: out_dict - days
                                       - hours
                                       - minutes
                                       - start_date
                                       - start_time
        """
        up = True
        out_dict = {}
        try:
            uptime = subprocess.Popen("uptime -p",stdout=subprocess.PIPE,shell=True)
            (out,error) = uptime.communicate()
            out = out.decode("utf-8").rstrip().split()
        except Exception as e:
            logging.error("Could not get uptime %s: %s"%error,e)
            up = False

        try:
            since = subprocess.Popen("uptime -s",stdout=subprocess.PIPE,shell=True)
            (sout,serror) = since.communicate()
            sout = sout.decode("utf-8").rstrip().split()
        except Exception as e:
            logging.error("Could not get uptime %s: %s"%serror,e)
            up = False
            
        #make the out data useful
        if(up):
            out_dict['days'] = out[1]
            out_dict['hours'] = out[3]
            out_dict['minutes'] = out[5]
            out_dict['start_date'] = sout[0]
            out_dict['start_time'] = sout[1]

        return out_dict

    def get_cpu_status(self):
        """
        DESC: Run the vcgencmd command and get some systme level stats
        INPUT: None
        OUTPUT: out_dict - cpu_temp
                                       - cpu_volts
                                       - ram_volts
                                       - io_volts
                                       - phy_volts
        """
        cmds = {'cpu_temp':'measure_temp','cpu_volts':'measure_volts core','ram_volts':'measure_volts sdram_c','io_volts':'measure_volts sdram_i','phy_volts':'measure_volts sdram_p','cpu_clock':'measure_clock arm'}
        output = {}
        
        for k,v in cmds.items():
            args = ['vcgencmd']
            args.append(v)
            try:
                cmd = subprocess.Popen(args, stdout=subprocess.PIPE)
                out = cmd.communicate()[0].decode("utf-8").rstrip().split('=')
                output[k] = out[1]
            except Exception as e:
                logging.error("vcgencmd: %s"%e)
                output[k] = 'ERROR'

        return output

    def get_network_status(self,nic=None):
        """
        DESC: Get the netwotk transmit recieve on the selected nic.
        INPUT: nic - nic name
        OUTPUT: out_dict - recieve
                         - transmit
        """
        if(nic is None):
            nic = settings.PHYSNET

        try:
            out = psutil.net_io_counters(pernic=True)
        except Exception as e:
            logging.error('Get network error: %s'%e)

        return out[nic]

    def get_memory(self):
        """
        DESC:  Get the cpu and gpu memory
        INPUT: None
        OUTPUT: out_dict - cpu_type
                                       - cpu_mem
                                       - gpu_mem
        """
        cmds = {'cpu_mem':'arm','gpu_mem':'gpu'}
        output = {}
        for k,v in cmds.items():
            args = ['vcgencmd','get_mem']
            args.append(v)
            try:
                cmd = subprocess.Popen(args, stdout=subprocess.PIPE)
                output[k] = cmd.communicate()[0].decode("utf-8").rstrip()
            except Exception as e:
                logging.error("vcgencmd: %s"%e)
                output[k] = 'ERROR'

        return output

    def get_system_status(self):
        """
        DESC: Get the system status metrics from the device.
        INPUT: None
        OUTPUT: out_dict - cpu_id
                                       - cpu_temp
                                       - cpu_voltage
                                       - cpu_clock
                                       - system_memory
                                       - system_uptime
                                       - network_tx_stats
                                       - network_rx_stats
        """
        cpu_stats = self.get_cpu_status()
        system_mem = self.get_memory()
        uptime = self.get_uptime()
        network = self.get_network_status()

        memory = system_mem['cpu_mem'].split('=')

        return {'cpu_id':self.get_cpu_id(),
                    'cpu_temp':cpu_stats['cpu_temp'],
                    'cpu_voltage':cpu_stats['cpu_volts'],
                    'cpu_clock':cpu_stats['cpu_clock'],
                    'system_memory':memory[1],
                    'system_uptime':uptime['days']+" days "+uptime['minutes']+" minutes",
                    'network_bytes_sent': network.bytes_sent,
                    'network_bytes_recv': network.bytes_recv
                    }

####MQTT######
    def send_mqtt(self,input_dict):
        """
        DESC: send the sensor readings to the mqtt broker
        INPUT: input_dict - sensor
                                      - temp
                                      - scale - F/C
                                      - humidity
        OUTPUT: None
        NOTE: None
        """
        #send a mesage to the MQTT broker, pub
        try:
            self.client.publish(settings.HOSTNAME+"/"+input_dict['sensor']+"/temperature",str(input_dict['temp'])+""+input_dict['scale'])
            self.client.publish(settings.HOSTNAME+"/"+input_dict['sensor']+"/humidity",str(input_dict['humidity']))
        except Exception as e:
            logging.error(e)
            logging.error("Could not send messages to MQTT broker")

    def recieve_mqtt(self,input_array):
        """
        INPUT: input_array - array of topics to subscribe to.
        """
        #get a message to the MQTT broker, sub 
        self.subscribe(input_array)

####DB#######
    def prune_db():
        pass

    def db_insert(self,input_dict):
        try:
            logging.info("Inserting sensor info into db. %s"%(input_dict))
            input_dict['date'] = str(datetime.datetime.now().timestamp())
            self.cursor.execute("INSERT INTO mqtt VALUES ('"+str(input_dict['temp'])+"','"+str(input_dict['humidity'])+"','"+input_dict['scale']+"','"+input_dict['sensor']+"','"+input_dict['date']+"')")
            self.sqlcon.commit()
        except Exception as e:
            logging.error(e)
            logging.error("Could not insert data into the database")

    def db_read():
        return {'output':'stuff'}

    def delete_record():
        pass

####System#####
    def write_config():
        pass