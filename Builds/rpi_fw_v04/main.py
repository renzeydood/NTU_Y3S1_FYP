from Ard_interface import *
from Camera_interface import *
from message_structure import *
import cv2
from Queue import Queue
from threading import Thread
import time

port = '/dev/ttyACM0'
baudrate = 19200
x = 0


class main():
    def __init__(self):
        #self.ard = Ard_interface(port, baudrate)
        self.cam = Camera_interface()
        self.msg_to_ard = SENDMessage()
        self.msg_from_ard = RCVDMessage()

        self.start = False
        self.stopCount = 0
        self.eCount = 0
        self.waitstart = True
        self.redlight = False

    def start_connection(self):
        #self.ard.connect()
        print("Arduino connected")
        self.cam.connect()
        print("Camera connected")

    def read_ard(self, pc_Q):
        while True:
            data = self.ard.usb_receive_message()
            if data:
                self.msg_from_ard = data
                print("***Received - type:", self.msg_from_ard.type, "id:",
                      self.msg_from_ard.id, "state:", self.msg_from_ard.type)
            time.sleep(0.2)

    def write_ard(self, d):
        # while True:
        #    if not ard_Q.empty():
        #        send = ard_Q.get()
        send = d
        print("**Writing:", send.construct())
        self.ard.usb_send_message(send)
        time.sleep(0.3)

    def init_thread(self):
        to_Ard_Q = Queue()
        to_PC_Q = Queue()

        #read_ard_thread = Thread(target=self.read_ard, args=(to_PC_Q,))
        """ write_ard_thread = Thread(target=self.write_ard, args=(to_Ard_Q,)) """
        display_cam_thread = Thread(target=self.display_cam)
        #logic_thread = Thread(target=self.logic, args=(to_Ard_Q, to_PC_Q))

        #read_ard_thread.start()
        """ write_ard_thread.start() """
        display_cam_thread.start()
        time.sleep(2)
        """ while(self.waitstart is True):
            if(raw_input("Type 'start' to start the robot->") == 'start'):
                logic_thread.start()
                self.waitstart = False """

        print("All threads started")

    def logic(self, ard_Q, pc_Q):
        # self.msg_to_ard.type = 'F'
        # ard_Q.put(self.msg_to_ard)
        # self.start = True

        # while self.start is True:
        while 1:
            print("Searching shapes")
            sign = self.cam.findShapes()
            print("*Logic -> Current sign:", sign)

            if(self.redlight is True):
                print("Waiting for green light!")
                if "Green light" in sign and self.msg_to_ard.type != '':
                    if "Right" in sign and self.msg_to_ard.type != 'R':
                        self.msg_to_ard.type = 'R'

                    elif "Left" in sign and self.msg_to_ard.type != 'L':
                        self.msg_to_ard.type = 'L'

                    else:
                        self.msg_to_ard.type = 'F'
                        self.msg_to_ard.motorspeed = 100

                    self.write_ard(self.msg_to_ard)
                    self.redlight = False

            elif(self.msg_from_ard.type != 'T'):
                if "Stop" in sign and self.msg_to_ard.type != 'S':
                    self.msg_to_ard.type = 'S'
                    # ard_Q.put(self.msg_to_ard)
                    self.write_ard(self.msg_to_ard)

                elif "Red light" in sign and self.msg_to_ard.type != 'S':
                    self.msg_to_ard.type = 'S'
                    self.write_ard(self.msg_to_ard)
                    self.redlight = True

                elif "Green light" in sign and self.msg_to_ard.type != '':
                    if "Right" in sign and self.msg_to_ard.type != 'R':
                        self.msg_to_ard.type = 'R'

                    elif "Left" in sign and self.msg_to_ard.type != 'L':
                        self.msg_to_ard.type = 'L'

                    else:
                        self.msg_to_ard.type = 'F'
                        self.msg_to_ard.motorspeed = 100

                    self.write_ard(self.msg_to_ard)

                if "Right" in sign and self.msg_to_ard.type != 'R':
                    self.msg_to_ard.type = 'R'
                    #self.msg_to_ard.type = 'R'
                    self.write_ard(self.msg_to_ard)

                if "Left" in sign and self.msg_to_ard.type != 'L':
                    self.msg_to_ard.type = 'L'
                    #self.msg_to_ard.type = 'L'
                    self.write_ard(self.msg_to_ard)

                elif "Clear" in sign and self.msg_to_ard.type != 'F':
                    self.stopCount = 0
                    self.msg_to_ard.type = 'F'
                    # ard_Q.put(self.msg_to_ard)
                    self.write_ard(self.msg_to_ard)

            if(self.msg_from_ard.type == 'E'):
                print("Object detected")

    def display_cam(self):
        while True:
            # self.cam.applyFilters()
            self.cam.displayFrame()
            #self.cam.displayColorFilters("red", 60)
            # self.cam.displayFilters("Thresh-Adaptive")
            #print("*Logic -> Current sign:", self.cam.findShapes())
            # self.cam.displayContours()
            if(cv2.waitKey(1) & 0xFF) == ord("q"):
                self.cam.close()
                print("Video steam ended")
                break

    def show_detected_shapes(self):
        while True:
            """ found = camera.findShapes()

            for shape in found:
                camera.drawShapes(shape) """
            camera.applyFilters()
            camera.display_frame()
            if(cv2.waitKey(1) & 0xFF) == ord("q"):
                camera.close()
                print("Video steam ended")
                break

    def stop_connection(self):
        self.ard.close()
        print("Arduino connected")
        self.cam.close()
        print("Camera connected")


if __name__ == "__main__":
    start = main()
    start.start_connection()
    start.init_thread()
