import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("irblaster.ddns.net", 6666))

print('SUCCESS: Connected to blaster server!')

s.close()

