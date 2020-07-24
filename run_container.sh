sudo docker run -d --device /dev/gpiomem -p 8883:8883 -v /opt/pitemp-local:/opt/pitemp --name pitemp \
-e SENSORTYP='DHT11' \
-e SCALE='Fahrenheit' \
-e PINS="24,23,4" \
-e SLEEP=2 \
-e RST='None' \
-e INTERVAL=1 \
-e PHYSNET='wlan0' \
-e MQTTBROKER='192.168.1.61' \
-e MQTTPORT='8883' \
-e SSLCERTPATH='/opt/pitemp/certs' \
-e SSLCERT='ca.crt' \
pitemp
