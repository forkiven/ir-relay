import weaver
import client
import reader
import atexit
import time

def main():

	# when started
	start_time = time.time()

	print('fetching proxy address...')
	# get weaver address
	proxyAddress = weaver.fetchProxyAddress().split('://')[1].split(':')
	TCP_IP = proxyAddress[0]
	TCP_PORT = int(proxyAddress[1])
	# Try to connect to server
	print('Connecting to socket @ ' + proxyAddress[0] + ':' + proxyAddress[1])
	client.socket.connect((TCP_IP, TCP_PORT))
	# Close socket on exit
	def closeSocket():
		client.socket.close()
	atexit.register(closeSocket)
	# Start reading signals
	while True:

		# if program has been running for more than 25 mins
		if int(time.time() - start_time) > 60:
			break

		binaryCode = reader.read()
		if binaryCode:
			# Send to server
			print('sent: ' + binaryCode)
			client.socket.send(binaryCode)

	# Close socket
	print('hit timeout...closing socket....')
	closeSocket()
	# delay to let socket terminate
	time.sleep(3)
	# restart
	main()

if __name__ == "__main__":
	main()