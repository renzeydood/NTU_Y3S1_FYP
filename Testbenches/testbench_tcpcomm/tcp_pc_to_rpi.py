from RPi_interface import *
from queue import Queue
from threading import Thread

class Main():
    def __init__(self):
        self.rpi = RPi_interface()
    
    def start_connection(self):
        #self.rpi.connect()
        print("RPi Connected")

    def read_rpi(self):
        self.rpi.read()

    def write_rpi(self):
        self.rpi.write()

    def init_thread(self):
        
        read_rpi_thread = Thread(target=self.rpi.read)
        write_rpi_thread = Thread(target=self.rpi.write)

        read_rpi_thread.start()
        write_rpi_thread.start()

        print("All threads started")

if __name__ == '__main__':
    start = Main()
    start.start_connection()
    start.init_thread()