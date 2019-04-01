from imutils.video.pivideostream import PiVideoStream
from datasets import DataSet
import imutils
import cv2
import numpy as np
import pickle as pk
import time


def pickle(name, data):
    pk_out = open(name, "w")
    pk.dump(data, pk_out)
    pk_out.close()


def unpickle(filename):
    pk_in = open(filename, "r")
    data = pk.load(pk_in)
    pk_in.close()


class LabTester(PiVideoStream):
    def __init__(self):
        PiVideoStream.__init__(self)
        self.ds = DataSet()
        self.clrSet_lab = self.ds.clrset_lab
        #self.clrSet_lab = unpickle("colorset_lab")

        self.panel = np.zeros([100, 700], np.uint8)
        cv2.namedWindow("Panel")

        cv2.createTrackbar("L", "Panel", 254, 508, self.nothing)
        cv2.createTrackbar("A", "Panel", 254, 508, self.nothing)
        cv2.createTrackbar("B", "Panel", 254, 508, self.nothing)

    def connect(self):
        self.start()  # Note that thread is already created for frame grabbing
        time.sleep(2.0)  # Warm up camera

    def displayFrame(self):
        #cv2.imshow("Camera view:", cv2.flip(self.frame, -1))
        cv2.imshow("Camera view:", self.frame)

    def displayFilters(self, select="Gray"):
        filters = {}
        output = self.frame

        filters["Original"] = output
        filters["Blur"] = cv2.GaussianBlur(output, (7, 7), 0)
        filters["Gray"] = cv2.cvtColor(filters["Blur"], cv2.COLOR_BGR2GRAY)
        filters["Thresh"] = cv2.threshold(
            filters["Gray"], 145, 255, cv2.THRESH_BINARY)[1]  # 60
        filters["Thresh-Adaptive"] = cv2.adaptiveThreshold(
            filters["Gray"], 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 5, 1)
        #filters["Thresh-Adaptive"] = cv2.dilate(filters["Thresh-Adaptive"], None, iterations=0)
        filters["Canny"] = cv2.Canny(filters["Blur"], 100, 200)
        filters["Canny-Auto"] = imutils.auto_canny(filters["Blur"])

        cv2.imshow("Camera view:", filters[select])

    def nothing(self, x):
        pass

    def color_set(self):
        clr = {
            "red": [182, 48, 66],
            "green": [51, 153, 51],
            "yellow": [255, 255, 0],
            "white": [255, 255, 255]
        }
        return clr

    def displayColorFilters(self, select="white", thresh=20):
        clr = self.color_set()["red"]
        lab = cv2.cvtColor(np.uint8([clr]), cv2.COLOR_RGB2LAB)[0][0]

        bar_l = cv2.getTrackbarPos("L", "Panel")
        bar_a = cv2.getTrackbarPos("A", "Panel")
        bar_b = cv2.getTrackbarPos("B", "Panel")

        lab[0] = lab[0] + (bar_l - 254)
        lab[1] = lab[1] + (bar_a - 254)
        lab[2] = lab[2] + (bar_b - 254)

        imageLAB = cv2.cvtColor(self.frame, cv2.COLOR_RGB2LAB)
        minLAB = np.array([lab[0] - thresh, lab[1] - thresh, lab[2] - thresh])
        maxLAB = np.array([lab[0] + thresh, lab[1] + thresh, lab[2] + thresh])
        val = cv2.inRange(imageLAB, minLAB, maxLAB)
        self.frame = val
        self.displayFrame()
        cv2.imshow("Panel", self.panel)

    def printColorInLAB(self, select="white"):
        clr = self.clrSet_lab[select]
        print("L*A*B values of {}: {}, {}, {}".format(select,
                                                      clr[0], clr[1], clr[2]))

    def close(self):
        self.stop()
