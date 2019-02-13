import socket
from message_structure import *
import struct
import time

host = '192.168.137.85'
port = 5000

class RPi_interface():
    def __init__(self):
        self.s = socket.socket()
        self.s.connect((host, port))
        self.msg = SENDMessage()

    def msgtosend(self):
        self.msg.type = 'S'
        self.msg.id = 1
        self.msg.distance = 50
        self.msg.motorspeed = 400
        self.msg.motorangle = 360
        print(START.encode(ARD_ENC))
        print(self.msg.type.encode(ARD_ENC))
        print(bytes([self.msg.id]))
        print(self.int_to_bytes(self.msg.distance))
        print(self.int_to_bytes(self.msg.motorspeed))
        print(self.int_to_bytes(self.msg.motorangle))
        return START.encode(ARD_ENC) + self.msg.type.encode(ARD_ENC) + bytes([self.msg.id]) + self.int_to_bytes(self.msg.distance) + self.int_to_bytes(self.msg.motorspeed) + self.int_to_bytes(self.msg.motorangle) + STOP.encode(ARD_ENC)

    def int_to_bytes(self, data):
        return bytes([data>>8]) + bytes([data&0xFF])

    def bytes_to_int(self, data):
        return struct.unpack('>h', data)[0]

    #Reading Message from RPi
    def write(self):
        #message = self.msgtosend()
        message = "This message is from PC to RPI".encode('utf-8')
        while True:
            print("Data to send:", message)
            self.s.sendall(message)
            #data = self.s.recv(1024).decode('utf-8')
            #print("Received from server: " + data)
            time.sleep(2)
        self.s.close()

    def read(self):
        while True:
            data = self.s.recv(1024)
            #print("Type of data:", type(data[0]))
            if not data:
                break
            print(data)
            for i in range(len(data)):
                if(data[i] == '!' and data[i+(MAX_BYTE_FROM_SERVER)] == '~'):
                    print("Valid data received")
                    print(data)
                    break
        self.s.close()

""" if __name__ == '__main__':
    print("Client started")
    client = Main()
    client.read() """