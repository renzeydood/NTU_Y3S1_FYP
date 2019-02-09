# interfaces the PC with the Raspberry Pi
import time
import socket
import datetime

class PCInterface:

    def __init__(self, host, port):
        # self.port = '/dev/ttyACM0'
        self.port = port
        # self.port='/dev/tty.usbmodem1421'
        self.serversock = socket.socket()  # create a new socket object
        self.serversock.bind((host, port))  # bind socket
        #self.serversock.setblocking(False)
        self.serversock.listen(1)
        self.received = []
        self.message_end = False

        print("Listening")

    # self.parity= serial.PARITY_ODD
    # self.bytesize=serial.SEVENBITS

    # Start and validate connection to PC
    def connect(self):
        clientsock, clientaddr = self.serversock.accept()
        print ("Connection from: " + str(clientaddr))
        while True:
            try:
                clientsock, clientaddr = self.serversock.accept()
                print("Connection from: " + str(clientaddr))
                return 1
            except:
                continue


    # Read message from PC
    def read(self):
        received = []
        try:
            data = self.clientsock.recv(1024)
            for i in range(len(data)):
                # if new line
                if (data[i] == 126):
                    message_end = True
                    print("Received from TCP: " + str(datetime.datetime.now()))
                    break
                received.append(data[i].to_bytes(1, byteorder='big'))
            return received, message_end
        except:
            return 0


    # Write message to PC
    def write(self, msg):
        self.clientsock.sendall(msg.encode("ascii"))

    def disconnect(self):
        self.serversock.close()
        print("TCP connection closed")
