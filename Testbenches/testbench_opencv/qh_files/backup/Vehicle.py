import threading
from SerialManager import SerialManager
from CameraManager import CameraManager


class Vehicle():

    def __init__(self, shape = 1, qr = 1):
        self.serialM = SerialManager()
        self.cam = CameraManager((shape, qr))





    def startCamera(self):
        #Start a camera thread for arrow finding
        self.camThread = threading.Thread(target = self.cam.captureFootage, args=(self.serialM.q,))
        self.camThread.start()


    def startSerial(self, rxCallBack, txCallBack):
        #start a serial thread to handle incoming comms

        self.serialRxThread = threading.Thread(target = self.serialM.incomingDataListener, args=(rxCallBack,))
        self.serialTxThread = threading.Thread(target = self.serialM.outBufferManager, args=(txCallBack,))
        self.serialRxThread.start()
        self.serialTxThread.start()
