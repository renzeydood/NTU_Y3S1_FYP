import threading
from SerialManager import SerialManager
from CameraManager import CameraManager



class Vehicle():

    #Entity class which is use to keep track of its installed modules in a Vehicle. More
    #modules can be added in to the vehicle by adding to this class.

    def __init__(self):
        self.serialM = SerialManager()
        self.cam = CameraManager()


    #======================Start the video camera app==================================
    #Function takes in user defined frame processing application as input and starts the
    #capturing/processing of the video in a new thread.
    #The user defined frame processing job will be run on every frame that is captured

    def startCamera(self, camApp):
        #Start a camera thread for vision applications
        self.camThread = threading.Thread(target = self.cam.captureFootage, args=(camApp,))
        self.camThread.start()

    #======================Start the serial reciever==================================
    #Function takes in user defined call-back function as input and starts a new thread
    #to handle incoming serial data.
    #The user defined call-back function will be run to process the incoming data. I.E
    #the call-back function will recieve the incoming data as parameter and processing will
    #be done as written in the function.

    def startSerial(self, rxCallBack):
        #start a serial thread to handle incoming comms
        self.serialRxThread = threading.Thread(target = self.serialM.incomingDataListener, args=(rxCallBack,))
        self.serialRxThread.start()
