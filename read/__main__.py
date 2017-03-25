#!/usr/bin/python

import reader
import atexit
import time
import socket
import RPi.GPIO as GPIO
import httplib2
import json
import datetime
import base64
import sys
import os
import getpass
import errno
from urllib2 import urlopen
from json import dumps
from socket import error as socket_error

# Weaved config
apiMethod="https://"
apiVersion="/v22"
apiServer="api.weaved.com"
apiKey="WeavedDemoKey$2015"

# Weaved User Login
userName = "mail@wumike.com"
password = "mikewu1209" 

# Weaved Device UID (irite-blaster)
UID = "80:00:00:05:46:02:D7:8B"

# HTTP settings
httplib2.debuglevel     = 0
http                    = httplib2.Http()
content_type_header     = "application/json"

# Login
# ===============================================
def login():

    loginURL = apiMethod + apiServer + apiVersion + "/api/user/login"

    loginHeaders = {
                'Content-Type': content_type_header,
                'apikey': apiKey
            }
    try:        
        response, content = http.request( loginURL + "/" + userName + "/" + password,
                                          'GET',
                                          headers=loginHeaders)
    except:
        print "Server not found.  Possible connection problem!"
        exit()                                          

    try: 
        data = json.loads(content)
        if(data["status"] != "true"):
            print "Can't connect to Weaved server!"
            print data["reason"]
            exit()

        token = data["token"]
    except KeyError:
        print "Connection failed!"
        exit()
        
    return token

# Proxy Connector
# ===============================================
def proxyConnect(token):

    # Host IP: This is equivalent to "whatismyip.com"
    my_ip = urlopen('http://ip.42.pl/raw').read()
    proxyConnectURL = apiMethod + apiServer + apiVersion + "/api/device/connect"

    proxyHeaders = {
                'Content-Type': content_type_header,
                'apikey': apiKey,
                'token': token
            }

    proxyBody = {
                'deviceaddress': UID,
                'hostip': my_ip,
                'wait': "true"
            }

    response, content = http.request( proxyConnectURL,
                                          'POST',
                                          headers=proxyHeaders,
                                          body=dumps(proxyBody),
                                       )
    try:
        return json.loads(content)["connection"]["proxy"]
    except KeyError:
        print "Key Error exception!"
        print content

# fetchProxyAddress
# ===============================================

def fetchProxyAddress():
    return proxyConnect(login())

def main():

	# Initialize GPIO for LED
	GPIO.setmode(GPIO.BOARD)
	# BOARD 16 = BCM 23
	GPIO.setup(16, GPIO.OUT)
	# Start with LED OFF
	GPIO.output(16, GPIO.LOW)

	# when started
	start_time = time.time()

	print('Fetching proxy address...')
	proxyAddress = fetchProxyAddress().split('://')[1].split(':')
	TCP_IP = proxyAddress[0]
	TCP_PORT = int(proxyAddress[1])
	# Try to connect to server
	print('Connecting to socket @ ' + proxyAddress[0] + ':' + proxyAddress[1])
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((TCP_IP, TCP_PORT))
	print('Waiting for signal...')
	# Turn LED ON
	GPIO.output(16, GPIO.HIGH)
	# Close socket on exit
	def closeSocket():
		s.close()
	atexit.register(closeSocket)
	# Start reading signals
	while True:

		# if program has been running for more than 25 mins
		if int(time.time() - start_time) > 1500:
			break

		binaryCode = reader.read()
		if binaryCode:
			# Flash LED
			GPIO.output(16, GPIO.LOW)
			time.sleep(0.1)
			GPIO.output(16, GPIO.HIGH)
			time.sleep(0.1)
			GPIO.output(16, GPIO.LOW)
			time.sleep(0.1)
			# Send to server
			print('sent: ' + binaryCode)
			s.send(binaryCode)
			# Turn LED back on - ready for new signal
			GPIO.output(16, GPIO.HIGH)

	# Close socket
	print('Timeout! Cleaning up and restarting...')
	closeSocket()
	# delay to let socket terminate
	# time.sleep(180)
	# restart
	main()

if __name__ == "__main__":
	main()