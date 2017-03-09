import weaver
import client
import atexit

def main():

	# get weaver address
	client.TCP_IP = weaver.fetchProxyAddress()
	# Try to connect to server
	print(client.TCP_IP)
	client.socket.connect((client.TCP_IP, client.TCP_PORT))

	# Close socket on exit
	def closeSocket():
		client.socket.close()
	atexit.register(closeSocket)

if __name__ == "__main__":
	main()