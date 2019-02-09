from ArduinoInterface import *
from BluetoothInterface import *
from PCInterface import *
import socket

from queue import Queue
from threading import Thread
import datetime
import os

""" Utilises 6 threads and 3 write queues. 
The 3 read threads will read from all components and pass to the respective queue.
The write threads will write data from the 3 queues to the components """


class Main(object):

    def __init__(self):
        os.system("sudo hciconfig hci0 piscan")
        self.arduino = ArduinoInterface(port='COM13',baud_rate=115200)
        self.android = BluetoothInterface()
        self.pc = PCInterface(host='',port='5000')
      
        pass

    def start_connection(self):
        try:
            self.arduino.connect()
            self.pc.connect()
            self.android.connect()
            print("All components connected!!")
            return 1
        except Exception as e:
            print("Error connecting: %", str(e))
            return 0

    #read data from ard and put to pc queue
    def read_ard(self, pc_queue):
        while True:
            temp = self.arduino.read()
            if temp is not None:
                string_to_send_tcp = ""
                for i in range(len(temp)):
                    string_to_send_tcp += temp[i].decode("ascii")
                pc_queue.put(string_to_send_tcp)

        # receives from Arduino, doesn't block
            """if (not from_arduino_queue.empty()):
                string_to_send_tcp = from_arduino_queue.get()
                print("Received from Arduino: " + str(datetime.datetime.now()))
                # Ends with a ~
                string_to_send_tcp += "~"
                print("sending to PC")
                print(string_to_send_tcp.encode("ascii"))"""


    #write to arduino from its own queue
    def write_ard(self, ard_queue):
        while True:
            if (not ard_queue.empty()):
                to_send_bytes = ard_queue.get()
                to_send_bytes.insert(0, bytes("~", "ascii"))
                to_send_bytes.append(bytes("!", "ascii"))
                self.arduino.write(b''.join(to_send_bytes))

    #read from pc and put to android queue or bluetooth queue depending on data
    def read_pc(self,to_android_queue, to_arduino_queue):
        while True:
            message_end = False
            while not message_end:
                received, message_end = self.pc.read()

                # pass to arduino queue
                # ONLY RECEIVES THESE TWO THINGS FROM PC = ARDUINO_INSTRUCTION((byte)(0x02)), ANDROID_UPDATE((byte)0x05);
                if message_end:
                    if (received[0] == (2).to_bytes(1, byteorder='big')):
                        print("Sends to Arduino: " + str(datetime.datetime.now()))
                        to_arduino_queue.put(received[1:4])
                        message_end = False
                        received = []

                # pass to bluetooth queue
                if(received[0] == (5).to_bytes(1, byteorder='big')):
                    to_android_queue.put()

    #write to pc from pc queue
    def write_pc(self,pc_queue):
        while True:
            if (not pc_queue.empty()):
                data = pc_queue.get()
                self.pc.write(data)


    def initialise(self):
        try:
            to_ard_queue = Queue()
            to_android_queue = Queue()
            to_pc_queue = Queue()

            read_ard_thread = Thread(target=self.read_ard, args=(to_pc_queue))
            write_ard_thread = Thread(target=self.write_ard, args=(to_ard_queue))

            read_android_thread = Thread(target=self.read_android, args=(to_pc_queue))
            write_android_thread = Thread(target=self.write_android, args=(to_android_queue))

            read_pc_thread = Thread(target=self.read_pc, args=(to_android_queue,to_ard_queue))
            write_pc_thread = Thread(target=self.write_pc, args=(to_pc_queue))


            read_ard_thread.start()
            write_ard_thread.start()
            read_android_thread.start()
            write_android_thread.start()
            read_pc_thread.start()
            write_pc_thread.start()

            print("All threads started!!")

        except Exception as e:
            print(str(e))
      


    def disconnect_all(self):
        try:
            self.android.disconnect()
            self.arduino.end_arduino_connection()
            self.pc.disconnect()
            return 1
        except Exception as e:
            print("Error disconnecting: %"  ,str(e))


if __name__ == "__main__":
    start = Main()
    start.start_connection()
    start.initialise()
   

