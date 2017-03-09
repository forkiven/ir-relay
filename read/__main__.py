import weaver
import client
import reader
import atexit
import time

start_time = time.time()

def main():

	# get weaver address
	proxyAddress = weaver.fetchProxyAddress().split('://')[1].split(':')
	TCP_IP = proxyAddress[0]
	TCP_PORT = int(proxyAddress[1])
	# Try to connect to server
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
			client.socket.send(binaryCode)

	# Close socket
	closeSocket()
	main()

if __name__ == "__main__":
	main()