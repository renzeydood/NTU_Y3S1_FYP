import socket

host = '192.168.137.209'
port = 4500

def PC_send():
	clientsock = socket.socket()
	clientsock.connect((host,port))

	data = input("Command for robot: ")
	while data != 'q':
		clientsock.send(data.encode('utf-8'))
		feedback = clientsock.recv(1024).decode('utf-8')
		print("Received: " + feedback)
		data = input("Command for robot: ")
		
	clientsock.close()

if __name__ == "__main__":	
	PC_send()
	
	