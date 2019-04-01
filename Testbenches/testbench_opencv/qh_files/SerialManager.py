import serial
import Queue

class SerialManager():

    #Control class to handle all things related to Serial Communication. Contain wrapper
    #method to abstractify the python Serial module. Allows for re-usabilility.

    def __init__(self):
        self.ser = serial.Serial('/dev/serial0', timeout=2)
        #Optional self mantain FIFO queue, use if needed
        self.q = Queue.Queue()

    #==========Serial TX function to wrap the python serial TX function==============
    #This is done to remove the dependency of the python serial module in other class

    def sendData(self, data):
        self.ser.write(data)

    #==========================RX data handler=======================================
    #Function can be run in a seperate thread to handle incoming serial data in the
    #background. User defined call-back function is required for post data processing.
    #Call-back mechanism is used to remove application specific instructions in this
    #class.

    def incomingDataListener(self, callBack):

        while True:
            if(self.ser.in_waiting != 0):
                data = self.ser.read()
                callBack(data)
