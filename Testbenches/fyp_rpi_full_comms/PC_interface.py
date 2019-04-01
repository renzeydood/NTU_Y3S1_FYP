import socket
from message_structure import *
import time
import struct

host = '192.168.137.85'
port = 5000

class PC_interface():
    def __init__(self):
        self.s = socket.socket()
        self.s.bind((host, port))
        self.s.listen(1)
        #self.c.setblocking(0)
        self.msg = RCVDMessage()
        print("Server initiated. Listening...")
        
    def connect(self):
        self.c, self.addr = self.s.accept()
        print("Connection from: " + str(self.addr))

    def int_to_bytes(self, data):
        return bytes([data>>8]) + bytes([data&0xFF])

    def bytes_to_int(self, data):
        return struct.unpack('>h', data)[0]

    #Reading message from PC
    def read(self):
        while True:
            data = self.c.recv(1024)
            if not data:
                break
            print(data)
            for i in range(len(data)):
                if(data[i] == '!' and data[i+(MAX_BYTE_FROM_CLIENT)] == '~'):
                    print("Valid data received")
                    print(data)
                    break
        self.c.close()

    def write(self):
        #message = self.msgtosend()
        message = "Hello, I'm RPi"
        while True:
            print("Data to send:", message)
            self.c.sendall(message)
            time.sleep(3)
        self.s.close()

    def disconnect(self):
        self.s.close()
        print("TCP connection closed")

""" if __name__ == '__main__':
    message = "Testing"
    server = Main(host, port)
    server.connect()
    #server.read()
    server.write(message)
    print("End") """