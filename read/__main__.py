import weaver
import client
import reader
import atexit

def main():

	# get weaver address
	client.TCP_IP = weaver.fetchProxyAddress()
	# Try to connect to server
	client.socket.connect(('proxy71.weaved.com', 39861))
	# Close socket on exit
	def closeSocket():
		client.socket.close()
	atexit.register(closeSocket)
	# Start reading signals
	while True:
		binaryCode = reader.read()
		if binaryCode:
			# Send to server
			client.send(binaryCode)

if __name__ == "__main__":
	main()