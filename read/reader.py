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

	# - Only care about the gaps (when pulse is a 1) so we filter our command array. 
	# - map (perform iterator function) so that if gap is greater than 1000, assume 1, else 0.
	# - Turn array into string using join()
	
	binaryString = ""
	gaps = filter(lambda x: x[0] == 1, command)
	for gap in gaps:

		if gap[1] < 1000:
			binaryString += "0"
		else:
			if gap[1] < 2000:
				binaryString += "1"

	# Return our binary code if we have one (minus whitespace)
	if binaryString.strip():
		return(binaryString)

if __name__ == "__main__":
	print(read())