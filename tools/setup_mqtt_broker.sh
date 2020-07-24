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

sudo cat /etc/mosquitto/mosquitto.conf <<EOF
pid_file /var/run/mosquitto.pid

persistence true
persistence_location /var/lib/mosquitto/

log_dest file /var/log/mosquitto/mosquitto.log

include_dir /etc/mosquitto/conf.d

listener 8883
cafile /etc/mosquitto/ca_certificates/ca.crt
keyfile /etc/mosquitto/ca_certificates/server.key
certfile /etc/mosquitto/ca_certificates/server.crt

EOF

sudo mosquitto -d -v -c /etc/mosquitto/mosquitto.conf
