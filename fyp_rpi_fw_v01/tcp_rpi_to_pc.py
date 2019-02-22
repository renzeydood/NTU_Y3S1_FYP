from PC_interface import *
from Queue import Queue
from threading import Thread

class Main():
    def __init__(self):
        self.pc = PC_interface()
    
    def start_connection(self):
        self.pc.connect()
        print("PC Connected")

    def read_pc(self):
        self.pc.read()

    def write_pc(self):
        self.pc.write()

    def init_thread(self):
        
        read_pc_thread = Thread(target=self.pc.read)
        write_pc_thread = Thread(target=self.pc.write)

        read_pc_thread.start()
        write_pc_thread.start()

        print("All threads started")

if __name__ == '__main__':
    start = Main()
    start.start_connection()
    start.init_thread()