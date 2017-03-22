import socket
import sys
import slinger

# Setup slinger
slinger.protocol = "NEC"
slinger.gpio_pin = 23
protocol_config = dict()        

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

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
            data = connection.recv(32)
            if data:
                print("Blast IR: " + data)
                if blasterReady:
                    blasterReady = False
                    ir = slinger.IR(slinger.gpio_pin, slinger.protocol, protocol_config)
                    ir.send_code(data)
                    blasterReady = True
            else:
                print >>sys.stderr, 'no more data from', client_address
                break
            
    finally:
        # Clean up the connection
        connection.close()

