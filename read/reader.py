#!/usr/bin/python

import RPi.GPIO as GPIO
import math
import os
from datetime import datetime
from time import sleep

# This is for revision 1 of the Raspberry Pi, Model B
# This pin is also referred to as GPIO23
INPUT_WIRE = 12

GPIO.setmode(GPIO.BOARD)
GPIO.setup(INPUT_WIRE, GPIO.IN)

def read():
	value = 1

	# Loop until we read a 0
	while value:
		value = GPIO.input(INPUT_WIRE)

	# Grab the start time of the command
	startTime = datetime.now()

	# Used to buffer the command pulses
	command = []

	# The end of the "command" happens when we read more than
	# a certain number of 1s (1 is off for my IR receiver)
	numOnes = 0

	# Used to keep track of transitions from 1 to 0
	previousVal = 0

	while True:

		if value != previousVal:
			# The value has changed, so calculate the length of this run
			now = datetime.now()
			pulseLength = now - startTime
			startTime = now

			command.append((previousVal, pulseLength.microseconds))

		if value:
			numOnes = numOnes + 1
		else:
			numOnes = 0

		# 10000 is arbitrary, adjust as necessary
		if numOnes > 10000:
			break

		previousVal = value
		value = GPIO.input(INPUT_WIRE)
	
	#print "----------Start----------"
	#for (val, pulse) in command:
		#print val, pulse
	
	binaryString = ""
	pulses = filter(lambda x: x[0] == 0, command)
	for pulse in pulses:

		pulseDuration = pulse[1]

		# Sony Protocol: 1 = pulse 1200 gap 600, 0 = pulse 600 gap 600
		if pulseDuration < 1000:
			binaryString += "0"
		else:
			# Ignore sony AGC (initial pulse) with 2400 duration
			if pulseDuration < 2000:
				binaryString += "1"			

	# Return our binary code if we have one (minus whitespace)
	if binaryString.strip():
		# Sony protocol that repeats - Only need first 20 bits
		irCode = binaryString[0:20]
		if len(irCode) == 20:
			# Anything less than 20 bits, assume white ir signal
			return irCode
		else:
			return False

if __name__ == "__main__":
	# Control LED
	GPIO.setup(16, GPIO.OUT)
	GPIO.output(16, GPIO.LOW)
	sleep(0.2)
	GPIO.output(16, GPIO.HIGH)
	print(read())
	GPIO.output(16, GPIO.LOW)