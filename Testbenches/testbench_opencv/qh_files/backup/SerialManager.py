import serial
import Queue
class SerialManager():



    def __init__(self):
        self.ser = serial.Serial('/dev/serial0', timeout=2)
        self.q = Queue.Queue()


    def sendData(self, data):
        self.ser.write(data)

    def outBufferManager(self, callBack):
        while True:
            #print "Q is empty: ", self.q.empty()
            while not self.q.empty():
                #print "Q data: ", self.q.get()
                data = self.q.get()
                callBack(data)



    def incomingDataListener(self, callBack):

        while True:
            if(self.ser.in_waiting != 0):
                data = self.ser.read()
                callBack(data)
