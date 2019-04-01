from lab_tester import *
import cv2
from threading import Thread


class main():
    def __init__(self):
        self.cam = LabTester()
        self.thiscolor = "white"

    def start_connection(self):
        self.cam.connect()
        print("Camera connected")

    def init_thread(self):
        display_cam_thread = Thread(target=self.display_cam)
        logic_thread = Thread(target=self.logic)

        display_cam_thread.start()
        time.sleep(2)
        logic_thread.start()

        print("All threads started")

    def logic(self):
        print("*****************************************")
        print("Select color: (Key in color name)")
        print("Print current L*A*B values: x")
        print("Save results: z")
        print("*****************************************")
        print("Current color: white")

        thiscolor = "white"

        while True:
            x = raw_input("->")
            if x == 'q':
                self.l = 10

            elif x == 'x':
                self.cam.printColorInLAB()

            elif x == 'white':
                self.thiscolor = "white"
                self.l = 0
                self.a = 0
                self.b = 0
                print("Current color: " + thiscolor)

            elif x == 'yellow':
                self.thiscolor = "yellow"
                self.l = 0
                self.a = 0
                self.b = 0
                print("Current color: " + thiscolor)

            elif x == 'red':
                self.thiscolor = "red"
                self.l = 0
                self.a = 0
                self.b = 0
                print("Current color: " + thiscolor)

            elif x == 'green':
                self.thiscolor = "green"
                self.l = 0
                self.a = 0
                self.b = 0
                print("Current color: " + thiscolor)

    def display_cam(self):
        while True:
            # self.cam.applyFilters()
            self.cam.displayColorFilters(select=self.thiscolor)
            # self.cam.displayFrame()
            #self.cam.displayColorFilters("red", 60)
            # self.cam.displayFilters("Thresh-Adaptive")
            #print("*Logic -> Current sign:", self.cam.findShapes())
            # self.cam.displayContours()
            if(cv2.waitKey(1) & 0xFF) == ord("t"):
                self.stop_connection()
                break

    def stop_connection(self):
        self.cam.close()
        print("Camera disconnected")


if __name__ == "__main__":
    start = main()
    start.start_connection()
    start.init_thread()
