#!/bin/bash -x
#NOTE: This is on raspbian
#generate the certificate authority key
openssl genrsa -aes128 -out ca.key -passout pass:mynewpassword 3072

#create a certificate
openssl req -new -passin pass:mynewpassword -x509 -days 2000 -key ca.key -out ca.crt -subj "/C=US/ST=Home/L=HOME/O=Global Security/OU=MQTT Department/CN=nothing.com"

#generate server keys pairs for the broker
openssl genrsa -out server.key 2048

#create the server csr
openssl req -new -out server.csr -key server.key -subj "/C=US/ST=Home/L=HOME/O=Global Security/OU=MQTT Department/CN=nothing.com"

#create the server cert signed with the ca key
openssl x509 -passin pass:mynewpassword -req -in server.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out server.crt -days 360
