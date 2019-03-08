from imutils.video.pivideostream import PiVideoStream
from datasets import DataSet
import imutils
import cv2
import numpy as np
import math
import time
import pickle as pk
from Shapes import Shapes

class Camera_interface(PiVideoStream):
    def __init__(self):
        PiVideoStream.__init__(self)
        self.ds = DataSet()
        self.clrSet_lab = self.ds.clrset_lab
        self.shapeSet_cnt = self.ds.shapeset_cnt

    def connect(self):
        self.start()            #Note that thread is already created for frame grabbing
        time.sleep(2.0)         #Warm up camera

    def displayFrame(self):
        #cv2.imshow("Camera view:", cv2.flip(self.frame, -1))
        cv2.imshow("Camera view:", self.frame)
        
    def drawShapes(self, shape):
        label = shape.getType() if shape.getOrientation() == None else shape.getType() + ": " + shape.getOrientation()
        c = shape.getContour()
        cv2.drawContours(cv2.flip(self.frame, -1), [c], -1, (0, 255, 0), 3)
        cv2.putText(cv2.flip(self.frame, -1), label, (c[0][0][0] - 100, c[0][0][1] - 35),
        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)

    def checkInRange(self, value, lower, upper):
        if lower <= value <= upper :
            return True
        return False

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

    def applyFilters(self, img, select="Gray"):
        filters = {}
        output = img

        filters["Original"] = output
        filters["Blur"] = cv2.GaussianBlur(output, (7, 7), 0)
        filters["Gray"] = cv2.cvtColor(filters["Blur"], cv2.COLOR_BGR2GRAY)
        filters["Thresh"] = cv2.threshold(filters["Gray"], 145, 255, cv2.THRESH_BINARY)[1]#60
        filters["Thresh-Adaptive"] = cv2.adaptiveThreshold(filters["Gray"], 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 1)
        filters["Thresh-Adaptive"] = cv2.erode(filters["Thresh-Adaptive"], None, iterations=0)
        filters["Canny"] = cv2.Canny(filters["Blur"], 100, 200)
        filters["Canny-Auto"] = imutils.auto_canny(filters["Blur"])

        return filters[select]

    def getContours(self, img):
        cnts = cv2.findContours(img.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        return cnts

    def compareWithShape(self, target, shape, thresh):
        res = cv2.matchShapes(target, shape, cv2.CONTOURS_MATCH_I3, 0)
        return True if res < thresh else False

    def compareWithColor(self, cnt, clr, thresh):
        image = self.frame
        mask = np.zeros(self.frame.shape, np.uint8)
        cv2.drawContours(mask, [cnt], -1, (255, 255, 255), thickness=cv2.FILLED)
        mask = self.applyFilters(mask, "Thresh")
        res = cv2.bitwise_and(self.frame, image, mask=mask)

        imageLAB = cv2.cvtColor(res, cv2.COLOR_RGB2LAB)
        minLAB = np.array([clr[0] - thresh, clr[1] - thresh, clr[2] - thresh])
        maxLAB = np.array([clr[0] + thresh, clr[1] + thresh, clr[2] + thresh])
        val = cv2.inRange(imageLAB, minLAB, maxLAB)
        return np.any(val), val

    def findShapes(self):
        filt_img = self.applyFilters(self.frame, "Thresh-Adaptive")
        #img_cnts = get_contours(filt_img)
        shaperesult = "Clear"

        _, cnts, h = cv2.findContours(filt_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        h = h[0]

        for b, c in enumerate(cnts):
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.04 * peri, True)#0.04

            if cv2.contourArea(c) > 100 and cv2.contourArea(c) < 100000:
                if ((len(approx) == 8) and self.compareWithShape(c, self.shapeSet_cnt["octagon"], 0.001)):
                    if (self.compareWithColor(c, self.clrSet_lab["red"], 20)):
                        #print("Stop sign detected")
                        shaperesult = "Stop " + str(cv2.contourArea(c))
                        cv2.drawContours(self.frame, [approx], -1, (240, 0, 159), thickness=2)
                
                elif ((len(approx) == 4) and self.compareWithShape(c, self.shapeSet_cnt["diamond"], 0.002)):
                    if (self.compareWithColor(c, self.clrSet_lab["yellow"], 20)):
                        #print("Slow sign detected")
                        shaperesult = "Slow " + str(cv2.contourArea(c))
                        cv2.drawContours(self.frame, [approx], -1, (240, 0, 159), thickness=2)

                elif (self.compareWithShape(c, self.shapeSet_cnt["circle"], 0.001)):
                    is_red, inner_red = self.compareWithColor(c, self.clrSet_lab["red"], 20)
                    is_green, inner_green = self.compareWithColor(c, self.clrSet_lab["green"], 20)

                    if(is_red):
                        #print("Traffic light: Red detected")
                        shaperesult = "Red light " + str(cv2.contourArea(c))

                    elif(is_green):
                        shaperesult = "Green light " + str(cv2.contourArea(c))
                        """ if(h[b, 2] != -1):
                            #print("Child exist")
                            _, ar = (self.compareWithColor(c, self.clrSet_lab["white"], 20))
                            ar_c = self.getContours(ar)
                            #print(len(ar_c))
                            for c_in in ar_c:
                                peri_in = cv2.arcLength(c_in, True)
                                approx_in = cv2.approxPolyDP(c_in, 0.04 * peri_in, True)#0.04
                                #print("Traffic light: Green with {} arrow detected".format(self.findArrow(ar_c, approx_in)))
                                cv2.drawContours(self.frame, [c_in], -1, (240, 0, 159), thickness=2)
                        else:
                            shaperesult = "Green light" """

                    cv2.drawContours(self.frame, [c], -1, (240, 0, 159), thickness=2)

                elif ((len(approx) == 7) and self.compareWithShape(c, self.shapeSet_cnt["arrow_r"], 0.1) and (h[b,3] == -1)):
                    if(self.compareWithColor(c, self.clrSet_lab["white"], 20)):
                        ar = self.findArrow(c, approx)
                        #print("{} arrow sign detected".format(ar))
                        shaperesult = "{} arrow ".format(ar) + str(cv2.contourArea(c))
                        cv2.drawContours(self.frame, [c], -1, (240, 0, 159), thickness=2)

        #self.displayFrame()
        #cv2.imshow("Camera view:", self.frame)

        return shaperesult

    def close(self):
        self.stop()