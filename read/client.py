import socket
import time

# IP to be determined via Weave API
TCP_IP = '127.0.0.1'

# Socket Port
TCP_PORT = 6666

# Buffer (amount of bytes)
MESSAGE = "Hello, World!"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))

messagesSent = 0

while True:
  s.send(MESSAGE)
  time.sleep(5)
  messagesSent += 1
  
  if messagesSent == 5:
    break
print("closing")
s.close()