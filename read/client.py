import socket
import time

# IP to be determined via Weave API
TCP_IP = '127.0.0.1'

# Socket Port
TCP_PORT = 6666

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)