from Ard_interface import *
from PC_interface import *
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
        self.ard = Ard_interface(port, baudrate)
        # self.pc = PC_interface()
        self.cam = Camera_interface()
        self.msg_to_ard = SENDMessage()
        self.msg_from_ard = RCVDMessage()

        self.start = False
        self.stopCount = 0
        self.eCount = 0
        self.waitstart = True
        self.redlight = False

    def start_connection(self):
        self.ard.connect()
        print("Arduino connected")
        """ self.pc.connect()
        print("PC Connected") """
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

    def read_pc(self):
        self.pc.read()

    def write_pc(self, pc_Q):
        self.pc.write()

    def init_thread(self):
        to_Ard_Q = Queue()
        to_PC_Q = Queue()

        read_ard_thread = Thread(target=self.read_ard, args=(to_PC_Q,))
        """ write_ard_thread = Thread(target=self.write_ard, args=(to_Ard_Q,)) """
        """ read_pc_thread = Thread(target=self.pc.read)
        write_pc_thread = Thread(target=self.pc.write) """
        display_cam_thread = Thread(target=self.display_cam)
        logic_thread = Thread(target=self.logicTest, args=(to_Ard_Q, to_PC_Q))

        read_ard_thread.start()
        """ write_ard_thread.start() """
        """ read_pc_thread.start()
        write_pc_thread.start() """
        display_cam_thread.start()
        time.sleep(4.5)
        while(self.waitstart is True):
            if(raw_input("Type 'start' to start the robot->") == 'start'):
                logic_thread.start()
                self.waitstart = False

        print("All threads started")

    def logicTest(self, ard_Q, pc_Q):
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

    def logic(self, ard_Q, pc_Q):

        # Send a starting message to arduino
        # if recieve, continue

        self.msg_to_ard.type = 'F'
        ard_Q.put(self.msg_to_ard)
        self.start = True

        while self.start is True:
            if self.msg_from_ard.type == 'S':
                sign = self.cam.findShapes()

                if "Stop" in sign:
                    self.stopCount = self.stopCount + 1

                elif "Clear" in sign:
                    self.stopCount = 0
                    self.msg_to_ard.type = 'F'

                if self.stopCount > 4:
                    # Wait for manual input
                    pass

                ard_Q.put(self.msg_to_ard)

            elif self.msg_from_ard.type == 'R':
                sign = self.cam.findShapes()

                if "Green light" in sign:
                    self.msg_to_ard.type = 'F'
                    self.msg_to_ard.motorspeed = 100

                    if "Right" in sign:
                        self.msg_to_ard.type = 'R'

                    elif "Left" in sign:
                        self.msg_to_ard.type = 'L'

                ard_Q.put(self.msg_to_ard)

            elif self.msg_from_ard.type == 'E':
                self.eCount = self.eCount + 1

                if self.eCount > 10:
                    # Switch to manual
                    pass
                pass

            elif self.msg_from_ard.type == 'T':
                # sign = self.cam.findShapes()
                print("Still turning")
                pass

            elif self.msg_from_ard.type == 'F':
                sign = self.cam.findShapes()
                print("*Logic -> Current sign:", sign)

                if "Clear" in sign:
                    self.msg_to_ard.type = 'F'

                elif "Stop" in sign:
                    self.msg_to_ard.type = 'S'

                elif "Red light" in sign:
                    self.msg_to_ard.type = 'S'

                elif "Green light" in sign:
                    self.msg_to_ard.type = 'F'
                    self.msg_to_ard.motorspeed = 100

                    if "Right" in sign:
                        self.msg_to_ard.type = 'R'

                    elif "Left" in sign:
                        self.msg_to_ard.type = 'L'

                elif "Slow" in sign:
                    self.msg_to_ard.type = 'F'
                    self.msg_to_ard.motorspeed = 50

                elif "Left arrow" in sign:
                    self.msg_to_ard.type = 'L'

                elif "Right arrow" in sign:
                    self.msg_to_ard.type = 'R'

                else:
                    self.msg_to_ard.type = 'F'

                ard_Q.put(self.msg_to_ard)

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
        """ self.pc.connect()
        print("PC Connected") """
        self.cam.close()
        print("Camera connected")


if __name__ == "__main__":
    start = main()
    start.start_connection()
    start.init_thread()
