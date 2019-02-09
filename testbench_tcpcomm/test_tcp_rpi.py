from PCInterface import *

host = ''
port = 0

class Main():
    def __init__(self):
        self.pc = PCInterface(host, port)
        self.pc.connect()


if __name__ == '__main__':
    Main()