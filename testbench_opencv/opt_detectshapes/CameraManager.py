import imutils
import cv2
import time
import numpy as np
import math
from Shapes import Shapes
from colordetector import ColorDetector

class CameraManager():

    def __init__(self, img=None):
        self.image = cv2.imread(img)
        self.image = imutils.resize(self.image, height=300)
        self.cd = ColorDetector()

    def loadImage(self, img):
        self.image = cv2.imread(img)

    def displayFrame(self, image):
        cv2.imshow("Image:", image)
        cv2.waitKey(0)

    def drawShapes(self, shape):
        label = shape.getType if shape.getOrientation() == None else shape.getType() + ": " + shape.getOrientation()
        c = shape.getContour()
        color = self.cd.label(self.image, c)
        cv2.drawContours(self.image, [c], -1, (0, 255, 0), 3)
        cv2.putText(self.image, str(label + color), (c[0][0][0] - 100, c[0][0][1] - 35), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)

    def checkInRange(self, value, lower, upper):
        if lower <= value <= upper:
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
            # self.drawShapes(c, potentialArrowOrient, approx[0][0])
            # if cv2.contourArea(c) > 12000:
            return potentialArrowOrient

        return None

    #======================Finding shapes in image frame============================
    #Function will return a list of shapes found in image frame

    def displayFiltered(self, select="Gray"):
        filters = {}
        output = self.image.copy()

        filters["Original"] = output
        filters["Blur"] = cv2.GaussianBlur(output, (3, 3), 0)
        filters["Gray"] = cv2.cvtColor(filters["Blur"], cv2.COLOR_BGR2GRAY)
        filters["Thresh"] = cv2.threshold(filters["Gray"], 115, 255, cv2.THRESH_BINARY)[1]#60
        filters["Thresh-Adaptive"] = cv2.adaptiveThreshold(filters["Gray"], 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2)
        filters["Canny"] = cv2.Canny(filters["Blur"], 100, 200)
        filters["Canny-Auto"] = imutils.auto_canny(filters["Blur"])

        output = filters[select]

        kernel = np.ones((3,3),np.uint8)
        #dilation = cv2.dilate(output, kernel, iterations=1)
        cl1 = cv2.morphologyEx(output, cv2.MORPH_CLOSE, kernel)
        closing = cv2.morphologyEx(output, cv2.MORPH_CLOSE, kernel)

        self.displayFrame(closing)

        return filters[select]

    def displayContours(self, filtered):
        cnts = cv2.findContours(filtered, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        output = self.image.copy()

        print(len(cnts)) #returns the number of contours found
        for c in cnts:
            if cv2.contourArea(c) > 110 and cv2.contourArea(c) < 10000:
                print("Area of contour: ", cv2.contourArea(c))
                cv2.drawContours(output, [c], -1, (240, 0, 159), 2)
                cv2.imshow("Contours", output)
                cv2.waitKey(0)

    def boundROI(self):
        (h, w, d) = self.image.shape
        roi = self.image[int(0.4*h):h, int(0.43*w):int(0.9*w)]      #Top left to bottom right
        return roi

    def findShapes(self):

        # Prep return value, default to None
        shapes = []
        # load the image, convert it to grayscale, blur it slightly,
        # and threshold it
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        #thresh = cv2.threshold(blurred, 150, 255, cv2.THRESH_BINARY)[1]#60 #150
        thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2)
        #self.image = thresh

        # find contours in the thresholded image
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if imutils.is_cv2() else cnts[1]

        for index, c in enumerate(cnts):
            debug = ''
            #debug = debug + "Contour area: " + str(cv2.contourArea(c))

            M = cv2.moments(c)
            if M["m00"] == 0:
                M["m00"] = 1
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])

            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.04 * peri, True)#0.04
            line = len(approx)

            #if( length == 7):
            if( line == 7 and (cv2.contourArea(c) < 5100.0) and (cv2.contourArea(c) > 4000.0)):
                arrowOrient = self.findArrow(c, approx)
                if arrowOrient != None:
                    shapes.append(Shapes("Arrow", c, arrowOrient))
                    debug = "Contour area: " + str(cv2.contourArea(c)) + " Shape: " + arrowOrient + " Arrow "

            elif(line == 8):
                shapes.append(Shapes("Stop Sign", c))
                debug = "Contour area: " + str(cv2.contourArea(c)) + " Shape: Stop Sign "

            elif(line == 0 and cv2.contourArea(c) > 200):
                shapes.append(Shapes("Circle", c))
                debug = "Contour area: " + str(cv2.contourArea(c)) + " Shape: Circle "

            print (debug + str(line))

            cv2.drawContours(self.image, [c], -1, (0, 255, 0), 2)
            cv2.imshow("Image", self.image)

            cv2.circle(self.image, (cX, cY), 7, (255, 0, 0), -1)

            #cv2.waitKey(0)

        return shapes
