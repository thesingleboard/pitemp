#lib file for pitemp
import subprocess
import datetime
import settings
import logging
import ssl
import sqlite3
import paho.mqtt.client as paho

class pitemp():
	
	def __init__(self):
		#connect to the mqtt broker
		self.client = paho.Client()
		self.client.tls_set(settings.SSLCERTPATH+"/"+settings.SSLCERT,tls_version=ssl.PROTOCOL_TLSv1_2)
		self.client.tls_insecure_set(True)
		
		try:
			#connect to the sqlite process
			sqlcon = sqlite3.connect('mqtt.db_%s'%(datetime.datetime.now().timestamp()))
			self.cursor = sqlcon.cursor()
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
	
	def prune_db():
		pass
	
	def db_insert(self,input_dict):
		try:
			input_dict['date'] = str(datetime.datetime.now().timestamp())
			self.cursor.execute("INSERT INTO mqtt VALUES ('"+str(input_dict['temp'])+"','"+str(input_dict['humidity'])+"','"+input_dict['scale']+"','"+input_dict['sensor']+"','"+input_dict['date']+"')")
		except Exception as e:
			logging.error(e)
			logging.error("Could not insert data into the database")
	
	def db_read():
		pass
	
	def delete_record():
		pass

