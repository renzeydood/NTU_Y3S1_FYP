import serial
import time
import serial.tools.list_ports
import struct
from message_structure import *

class Ard_interface():
    def __init__(self, port, baudrate):
        self.port = port
        self.baudrate = baudrate
        self.ser = None
        self.packetcounter = 0;

        self.msgRCVD = RCVDMessage()
        self.msgSEND = SENDMessage()

    def connect(self):
        print("Connecting to Arduino...")
        try:
            self.ser = serial.Serial(self.port, self.baudrate)
            if self.ser.isOpen():
                self.ser.setDTR(False)
                time.sleep(1)
                self.ser.flush()
                self.ser.setDTR(True)
                print("Connection to Arduino successful")

        except serial.SerialException as e:
            print("Connection to Arduino, ", self.port, "failed. Error:", e)

    def int_to_bytes(self, data):
        return chr(data>>7) + chr(data&0x7F)

    def bytes_to_int(self, u, l):
        return u<<7 | l

    #This fuction should be placed in the remote pc controller, not in RPi
    def usb_send_message(self, data):
        #msg = (START + data[0] + chr(data[1]) + self.int_to_bytes(data[2]) + self.int_to_bytes(data[3]) + self.int_to_bytes(data[4]) + STOP).encode()
        #self.ser.write(msg)
        self.ser.write(data.construct())
        self.ser.flush()
        print("Message to Arduino sent.")
        #print("Message:", msg)
        print("Message:", data.construct())

    def usb_receive_message(self):
        if(self.ser.inWaiting() > 0):
            tempBytes = self.ser.read()
            if(tempBytes == bytes(START.encode())):
                data = []
                counter = 0
                while True:
                    nextByte = self.ser.read()
                    if(nextByte == bytes(STOP.encode()) and counter == MAX_BYTE_FROM_SERVER-1):
                        return self.msgRCVD.destruct(data)
                        #return data
                    else:
                        data.append(nextByte)
                    counter = counter + 1
        return None

    def update_counter(self):
        if(self.packetcounter <= 127):
            self.packetcounter = 0
        else:
            self.packetcounter = self.packetcounter + 1

    def close(self):
        self.ser.close()
        print("Connection to Arduino closed")

    def reconnect(self):
        self.close()
        self.connect()