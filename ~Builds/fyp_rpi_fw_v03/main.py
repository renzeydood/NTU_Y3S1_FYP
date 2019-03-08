from Ard_interface import *
from PC_interface import *
from Camera_interface import *
from message_structure import *
import cv2
from Queue import Queue
from threading import Thread

port = '/dev/ttyACM0'
baudrate = 9600
x = 0

class main():
    def __init__(self):
        self.ard = Ard_interface(port, baudrate)
        #self.pc = PC_interface()
        self.cam = Camera_interface()
        self.msg_to_ard = SENDMessage()
        self.msg_from_ard = RCVDMessage()

        self.stopCount = 0
        self.eCount = 0

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
                print("***Received - type:", self.msg_from_ard.type, "id:", self.msg_from_ard.id, "state:", self.msg_from_ard.type)
            time.sleep(0.2)

    def write_ard(self, ard_Q):
        while True:
            if not ard_Q.empty():
                send = ard_Q.get()
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
        write_ard_thread = Thread(target=self.write_ard, args=(to_Ard_Q,))
        """ read_pc_thread = Thread(target=self.pc.read)
        write_pc_thread = Thread(target=self.pc.write) """
        display_cam_thread = Thread(target=self.display_cam)
        logic_thread = Thread(target=self.logic, args=(to_Ard_Q, to_PC_Q))

        read_ard_thread.start()
        write_ard_thread.start()
        """ read_pc_thread.start()
        write_pc_thread.start() """
        display_cam_thread.start()
        logic_thread.start()

        print("All threads started")

    def logic(self, ard_Q, pc_Q):

        #Send a starting message to arduino
        #if recieve, continue
        self.msg_to_ard.type = 'A'
        ard_Q.put(self.msg_to_ard)

        while self.msg_from_ard.type != 'I':
            if self.msg_from_ard == 'F':
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

            elif self.msg_from_ard == 'T':
                #sign = self.cam.findShapes()
                pass

            elif self.msg_from_ard == 'S':
                sign = self.cam.findShapes()

                if "Stop" in sign:
                    self.stopCount = self.stopCount + 1

                elif "Clear" in sign:
                    self.stopCount = 0
                    self.msg_to_ard.type = 'F'

                if self.stopCount > 4:
                    #Wait for manual input
                    pass
                
                ard_Q.put(self.msg_to_ard)
            
            elif self.msg_from_ard == 'R':
                sign = self.cam.findShapes()

                if "Green light" in sign:
                    self.msg_to_ard.type = 'F'
                    self.msg_to_ard.motorspeed = 100

                    if "Right" in sign:
                        self.msg_to_ard.type = 'R'

                    elif "Left" in sign:
                        self.msg_to_ard.type = 'L'

                ard_Q.put(self.msg_to_ard)

            elif self.msg_from_ard == 'E':
                self.eCount = self.eCount + 1

                if self.eCount > 10:
                    #Switch to manual
                    pass
                pass

    def display_cam(self):
        while True:
            #self.cam.applyFilters()
            self.cam.displayFrame()
            if(cv2.waitKey(1)&0xFF)==ord("q"):
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
            if(cv2.waitKey(1)&0xFF)==ord("q"):
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