#!/usr/bin/python

import reader
import atexit
import time
import socket
import RPi.GPIO as GPIO

def main():

	# Initialize GPIO for LED
	GPIO.setmode(GPIO.BOARD)
	# BOARD 16 = BCM 23
	GPIO.setup(16, GPIO.OUT)
	# Start with LED OFF
	GPIO.output(16, GPIO.LOW)

	# when started
	start_time = time.time()

	TCP_IP = "irblaster.ddns.net"
	TCP_PORT = 6666

	# Connect to TCP Server
	def connect():
		global irc
		irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		irc.connect((TCP_IP, TCP_PORT))
		print('CONNECTED: Waiting for signal...')

	connect()

	# Turn LED ON
	GPIO.output(16, GPIO.HIGH)

	# Close socket on exit
	atexit.register(irc.close())

	# Start reading and sending. This part should run forever.
	while True:

		# Try to read a signal
		binaryCode = reader.read()
		if binaryCode:

			# Flash LED to indicate successfully read signal
			GPIO.output(16, GPIO.LOW)
			time.sleep(0.1)
			GPIO.output(16, GPIO.HIGH)
			time.sleep(0.1)
			GPIO.output(16, GPIO.LOW)
			time.sleep(0.1)

			# Send to server
			irc.send(binaryCode)
			print('SIGNAL SENT: ' + binaryCode)

			# Get response from server
			serverResponse = irc.recv(12)
			if serverResponse:
				print(serverResponse)		
			else:
				# If we get no response, reconnect.
				print("NO SERVER RESPONSE: Reconnecting...")
				irc.close()
				connect()				
							
			# Turn LED back on - ready for new signal
			GPIO.output(16, GPIO.HIGH)


if __name__ == "__main__":
	main()