import weaver
import client
import reader
import atexit

def main():

	# get weaver address
	client.TCP_IP = weaver.fetchProxyAddress()
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
		binaryCode = reader.read()
		if binaryCode:
			# Send to server
			client.socket.send(binaryCode)

if __name__ == "__main__":
	main()