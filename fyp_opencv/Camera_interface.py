from imutils.video.pivideostream import PiVideoStream
import imutils
import cv2
import numpy as np
import math
import time
from Shapes import Shapes

class Camera_interface(PiVideoStream):
    def __init__(self):
        PiVideoStream.__init__(self)
        pass

    def connect(self):
        self.start()     #Note that thread is already created for fram grabbing
        time.sleep(2.0)         #Warm up camera

    def display_frame(self):
        #cv2.imshow("Camera view:", self.frame)
        cv2.imshow("Camera view:", self.applyFilters())

    #======================Helper function for drawing of shapes and labels==================================

    def drawShapes(self, shape):

        label = shape.getType() if shape.getOrientation() == None else shape.getType() + ": " + shape.getOrientation()
        c = shape.getContour()
        cv2.drawContours(self.frame, [c], -1, (0, 255, 0), 3)
        cv2.putText(self.frame, label, (c[0][0][0] - 100, c[0][0][1] - 35),
        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)

    #======================Helper function for range checking==================================================

    def checkInRange(self, value, lower, upper):
        if lower <= value <= upper :
            return True
        return False

    #======================Convert the gradient angle of two lines of a point to it's potential orientation==================================
    #The angle of the two lines of a point will determine if that particular point is a tip of an arrow. The orientation will depend on the
    #matching to a pre-calculated pair of angles as shown in the table below:

    #Angle 1    Angle 2     Orientation
    #-------------------------------------
    #135       -135         Left
    #-45       -45          Right
    #-135      -45          Up
    #45        135          Down

    #Reference: https://stackoverflow.com/questions/22876351/opencv-2-4-8-python-determining-orientation-of-an-arrow

    def angleToTipOrientation(self, anglePair):

        #Tolerence value for inaccracy in angle calculations
        tolerance = 10;

        if self.checkInRange(anglePair[0], 135-tolerance, 135+tolerance) and self.checkInRange(anglePair[1], -(135+tolerance), -(135-tolerance)):#135 && -135
            return "Left"
        elif self.checkInRange(anglePair[0], -(45+tolerance), -(45-tolerance) ) and self.checkInRange(anglePair[1], 45-tolerance, 45+tolerance):#-45 && 45
            return "Right"
        elif self.checkInRange(anglePair[0], -(135+tolerance), -(135-tolerance)) and self.checkInRange(anglePair[1], -(45+tolerance), -(45-tolerance)):#-135 && -45
            return "Up"
        elif self.checkInRange(anglePair[0], 45-tolerance, 45+tolerance) and self.checkInRange(anglePair[1], 135-tolerance, 135+tolerance):#45 && 135
            return "Down"
        else: return None

    def findArrow(self, c, approx):
        potentialArrowOrient = None
        rightAngleCounter = 0;

        if len(approx) == 7:

            for index, m in enumerate(approx):

                if index == 0:
                    line1Subtract = np.subtract(m, approx[6])
                    line2Subtract = np.subtract(m, approx[1])
                elif index == 6:
                    line1Subtract = np.subtract(m, approx[5])
                    line2Subtract = np.subtract(m, approx[0])
                else:
                    line1Subtract = np.subtract(m, approx[index -1])
                    line2Subtract = np.subtract(m, approx[index + 1])
                angle1 = math.atan2(line1Subtract[0][1], line1Subtract[0][0])*180/np.pi
                angle2 = math.atan2(line2Subtract[0][1], line2Subtract[0][0])*180/np.pi
                tipOrientation = self.angleToTipOrientation((angle1,angle2))
                potentialArrowOrient = potentialArrowOrient if tipOrientation == None else tipOrientation
                ptAngle = abs(angle1 + angle2)

                if abs(ptAngle) < 25 or abs(ptAngle - 90) < 25 or abs(ptAngle - 180) < 25 or abs(ptAngle - 270) < 25 :
                    rightAngleCounter+=1


        if(rightAngleCounter == 5 and potentialArrowOrient != None):
            return potentialArrowOrient

        return None

    def applyFilters(self):
        gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]#60

        return thresh

    #======================Finding shapes in image frame============================
    #Function will return a list of shapes found in image frame

    def findShapes(self):

        # Prep return value, default to None
        shapes = []
        # load the image, convert it to grayscale, blur it slightly,
        # and threshold it
        gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]#60

        # find contours in the thresholded image
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)

        for index, c in enumerate(cnts):

            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.04 * peri, True)#0.04
            length = len(approx)
            if( length == 7):
                arrowOrient = self.findArrow(c, approx)
                if arrowOrient != None:
                    shapes.append(Shapes("Arrow", c, arrowOrient))

            """ elif( length == 8):
                shapes.append(Shapes("Stop Sign", c, None))

            elif(length == 0 and cv2.contourArea(c) > 200):
                shape = Shapes("Circle", c, None) """

        return shapes    

    def close(self):
        self.stop()