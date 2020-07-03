#!/bin/bash -x
#NOTE: This is on raspbian
#generate the certificate authority key
openssl genrsa -aes128 -out ca.key -passout pass:mynewpassword 3072

#create a certificate
openssl req -new -x509 -days 2000 -key ca.key -out ca.crt

#generate server keys pairs for the broker
openssl genrsa -out server.key 2048

#create the server csr
openssl req -new -out server.csr -key server.key -subj "/C=US/ST=Home/L=HOME/O=Global Security/OU=MQTT Department/CN=nothing.com"

#create the server cert signed with the ca key
openssl x509 -req -in server.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out server.crt -days 360

#copy the ca.crt server.crt and the server.key to ca certs file for your broker
# cp ca.crt /etc/mosquitto/ca_certificates/
# cp server.crt /etc/mosquitto/ca_certificates/
# cp server.key /etc/mosquitto/ca_certificates/

# set broker listener port to 8883 in mosquitto.conf


#openssl req -nodes -newkey rsa:2048 -keyout mqtt_key.key -out mqtt_csr.csr -subj "/C=US/ST=Home/L=HOME/O=Global Security/OU=MQTT Department/CN=nothing.com"
#openssl x509 -req -days 365 -in ./mqtt_csr.csr -signkey ./mqtt_key.key -out mqtt_cert.crt
