from Ard_interface import *
from Queue import Queue
from threading import Thread
import time

port = '/dev/ttyACM0'
baudrate = 9600
x = 0

class Main():
    def __init__(self):
        self.ard = Ard_interface(port, baudrate)

    def start_connection(self):
        self.ard.connect()
        print("Arduino connected")

    def read_ard(self):
        
        while True:
            print("******Read arduino thread")
            data = self.ard.usb_receive_message()
            if not data:
                print("Data not found")
            else:
                print(data)
            time.sleep(0.8)

    def write_ard(self):
        #data = ['A', 1, 50, 400, 360]
        global x
        if(x == 0):
            data = b'\x21\x41\x01\x00\x32\x01\x90\x01\x68\x7E'
            x = 1;
        else:
            data = b'\x21\x41\x01\x00\xFA\x00\x64\x01\xB4\x7E'
            x = 0;
        
        while True:
            print("******Write arduino thread")
            self.ard.usb_send_message(data)
            time.sleep(2)

    def init_thread(self):
        read_ard_thread = Thread(target=self.read_ard)
        write_ard_thread = Thread(target=self.write_ard)

        read_ard_thread.start()
        write_ard_thread.start()

        print("All threads started")


if __name__ == "__main__":
    ard = Main()
    ard.start_connection()
    ard.init_thread()
    #ard.read_ard()