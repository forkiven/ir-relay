#!/usr/bin/python

import socket
import sys
import slinger
from datetime import datetime

# Setup slinger
slinger.protocol = "Sony"
slinger.gpio_pin = 23
protocol_config = dict()
# Sony Protocol Bit Length
bitLength = 20        

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Re-use socket
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Bind the socket to the port
server_address = ("", 6666)
print >>sys.stderr, 'starting up on %s port %s' % server_address
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

blasterReady = True

while True:
    # Wait for a connection
    print >>sys.stderr, 'waiting for a connection'
    connection, client_address = sock.accept()

    try:
        print >>sys.stderr, 'connection from', client_address

        # Receive the data in small chunks and retransmit it
        while True:
            data = connection.recv(bitLength)
            if data:
                print("Received code: " + data)
                timeReceived = datetime.now()
                ir = slinger.IR(slinger.gpio_pin, slinger.protocol, protocol_config)
                ir.send_code(data)
                print("Time taken to blast: " + str((datetime.now() - timeReceived).microseconds))
                connection.send("pong")
            else:
                print >>sys.stderr, 'no more data from', client_address
                break
            
    finally:
        # Clean up the connection
        connection.close()