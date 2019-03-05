from Ard_interface import *
from PC_interface import *
#from Camera_interface import *
from message_structure import *
#import cv2
from Queue import Queue
from threading import Thread

port = '/dev/ttyACM2'
baudrate = 9600
x = 0

class main():
    def __init__(self):
        self.ard = Ard_interface(port, baudrate)
        #self.pc = PC_interface()
        #self.cam = Camera_interface()
        self.msg_to_ard = SENDMessage()
        self.msg_from_ard = RCVDMessage()

    def start_connection(self):
        self.ard.connect()
        print("Arduino connected")
        """ self.pc.connect()
        print("PC Connected") """
        """ self.cam.connect()
        print("Camera connected") """

    def read_ard(self, Q):
        while True:
            print("******Read arduino thread")
            data = self.ard.usb_receive_message()
            if data:
                self.msg_from_ard = data
                print("Received type:", self.msg_from_ard.type)
                print("Received id:", self.msg_from_ard.id)
                print("Received state:", self.msg_from_ard.type)
                #print(data)
            time.sleep(1.4)

    def write_ard(self, Q):
        while True:
            #print("******Write arduino thread")
            if not Q.empty():
                self.ard.usb_send_message(Q.get())
            time.sleep(2.2)

    def read_pc(self):
        self.pc.read()

    def write_pc(self, Q):
        self.pc.write()

    def init_thread(self):
        to_Ard_Q = Queue()
        to_PC_Q = Queue()

        read_ard_thread = Thread(target=self.read_ard, args=(to_PC_Q,))
        write_ard_thread = Thread(target=self.write_ard, args=(to_Ard_Q,))
        """ read_pc_thread = Thread(target=self.pc.read)
        write_pc_thread = Thread(target=self.pc.write) """
        #display_cam_thread = Thread(target=self.display_cam)
        logic_thread = Thread(target=self.logic_test, args=(to_Ard_Q, to_PC_Q))

        read_ard_thread.start()
        write_ard_thread.start()
        """ read_pc_thread.start()
        write_pc_thread.start() """
        #display_cam_thread.start()
        logic_thread.start()

        print("All threads started")

    def logic_test(self, ard_Q, pc_Q):
        """
        check if robot is idle
        if idle, send message
        else, wait, unless must send emergency instruction
        """
        self.msg_to_ard.type = 'L'
        ard_Q.put(self.msg_to_ard)
        time.sleep(2.2)
        self.msg_to_ard.type = 'R'
        ard_Q.put(self.msg_to_ard)
        time.sleep(2.2)
        self.msg_to_ard.type = 'S'
        ard_Q.put(self.msg_to_ard)
        time.sleep(2.2)
        pass

    def logic(self, Q):
        while(True):
            shapesFound = self.cam.findShapes()
            currentShape = ''
            stop = False
            go = False
            arrow = False
            index = 0

            for shape in shapesFound:
                self.cam.drawShapes(shape) 
                if shape.type == "Stop Sign":
                    stop = True
                if shape.type == "Circle":
                    stop = True
                if shape.type == "Arrow":
                    stop = True
                index = index + 1

            if stop == True:
                print("Stop")
                Q.put(['S', 0, 0, 0, 0])

            elif go == True:
                print("Go")
                Q.put(['F', 0, 0, 0, 0])

            elif arrow == True:
                if shapesFound[index].orientation == "Left":
                    print("Turn left")
                    Q.put(['L', 0, 0, 0, 0])

                elif shapesFound[index].orientation == "Right":
                    print("Turn right")
                    Q.put(['R', 0, 0, 0, 0])
            
            else:
                print("No shapes found")
                Q.put(['S', 0, 0, 0, 0])

            time.sleep(0.8)

    def display_cam(self):
        while True:
            #self.cam.applyFilters()
            self.cam.display_frame()
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

if __name__ == "__main__":
    start = main()
    start.start_connection()
    start.init_thread()