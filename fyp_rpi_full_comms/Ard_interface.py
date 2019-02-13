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
        return bytes([data>>8]) + bytes([data&0xFF])

    def bytes_to_int(self, data):
        return struct.unpack('>h', data)[0]

    #This fuction should be placed in the remote pc controller, not in RPi
    def usb_send_message(self, data):
        #msg = START.encode(ARD_ENC) + data[0].encode(ARD_ENC) + bytes([data[1]]) + self.int_to_bytes(data[2]) + self.int_to_bytes(data[3]) + self.int_to_bytes(data[4]) + STOP.encode(ARD_ENC)
        msg = data
        #try:
        self.ser.write(msg)
        self.ser.flush()
        print("Message to Arduino sent.")
        print("Message:", msg)
        #except Exception as e:
        #    print("Error: " + str(e))
        #    self.reconnect()

    def usb_receive_message(self):
        if(self.ser.inWaiting() > 0):
            tempBytes = self.ser.read()
            if(tempBytes == bytes(START.encode())):
                data = []
                counter = 0
                while True:
                    nextByte = self.ser.read()
                    if(nextByte == bytes(STOP.encode()) and counter == MAX_BYTE_FROM_SERVER-1):
                        #print(data)
                        #print(self.bytes_to_int(data[3] + data[4]))
                        return data
                    else:
                        data.append(nextByte)
                    if(counter == MAX_BYTE_FROM_SERVER-1):
                        print(data)
                    counter = counter + 1
        return None

    def close(self):
        self.ser.close()
        print("Connection to Arduino closed")

    def reconnect(self):
        self.close()
        self.connect()