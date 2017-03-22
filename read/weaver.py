#!/usr/bin/python

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
import socket

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

if __name__ == "__main__":
    address = fetchProxyAddress().split('://')[1].split(':')
    url = address[0]
    port = address[1]
    print("address: " + url)
    print("port: " + port)