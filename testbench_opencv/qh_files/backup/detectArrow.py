# import the necessary packages

import imutils
import cv2
import time
import numpy as np
import math
from picamera.array import PiRGBArray
from picamera import PiCamera


def checkInRange(value, lower, upper):
    if lower <= value <= upper :
        return True
    return False

def angleToTipOrientation(anglePair):

    tolerance = 10;
    #print "anglepair: ", anglePair[0], " ", anglePair[1]
    print "checkInRange(anglePair[0], -(45+tolerance), -(45-tolerance)): ", checkInRange(anglePair[0], -(45+tolerance), -(45-tolerance))
    print "checkInRange(anglePair[1], -(135+tolerance), -(135-tolerance))", checkInRange(anglePair[1], -(135+tolerance), -(135-tolerance))
    
    if checkInRange(anglePair[0], 135-tolerance, 135+tolerance) and checkInRange(anglePair[1], -(135+tolerance), -(135-tolerance)):#135 && -135
        return "Arrow facing left"
    elif checkInRange(anglePair[0], -(45+tolerance), -(45-tolerance) ) and checkInRange(anglePair[1], 45-tolerance, 45+tolerance):#-45 && 45
        return "Arrow facing right"
    elif checkInRange(anglePair[0], -(135+tolerance), -(135-tolerance)) and checkInRange(anglePair[1], -(45+tolerance), -(45-tolerance)):#-135 && -45
        return "Arrow facing up"
    elif checkInRange(anglePair[0], 45-tolerance, 45+tolerance) and checkInRange(anglePair[1], 135-tolerance, 135+tolerance):#45 && 135
        return "Arrow facing down"
    else: return None  

#======================Determine if contour is an arrow=============
def findArrow(c):
    potentialArrowOrient = None
    rightAngleCounter = 0;
    peri = cv2.arcLength(c, True)
    print "Peri: ", peri
    approx = cv2.approxPolyDP(c, 0.04 * peri, True)#0.04
    print "len(approx): ", len(approx)
    if len(approx) == 7:

        for index, m in enumerate(approx):

            print "Point: ", m
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
            tipOrientation = angleToTipOrientation((angle1,angle2))
            potentialArrowOrient = potentialArrowOrient if tipOrientation == None else tipOrientation
            ptAngle = abs(angle1 + angle2)
            print "Angle1: ", angle1
            print "Angle2: ", angle2
            print "Combine angle: ", ptAngle

            if abs(ptAngle) < 25 or abs(ptAngle - 90) < 25 or abs(ptAngle - 180) < 25 or abs(ptAngle - 270) < 25 :
                rightAngleCounter+=1
                print "Right Angle: True"
            else:
                print "Right Angle: False"
            print "\n"
            #cv2.putText(filtered, str(m), (m[0][0], m[0][1]),
            #cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255) , 1)
            
    if(rightAngleCounter == 5):
        print "ARROW DETECTED"
        print potentialArrowOrient;
        cv2.drawContours(image, [c], -1, (0, 255, 0), 3)
        cv2.imshow("Arrow", image)
        cv2.waitKey(0)
    
#===================================================================================================================

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
rawCapture = PiRGBArray(camera)
# allow the camera to warmup
#time.sleep(0.1)

# grab an image from the camera
camera.capture(rawCapture, format="bgr")
image = rawCapture.array

# load the image, convert it to grayscale, blur it slightly,
# and threshold it
#image = cv2.imread(args["image"])
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY_INV)[1]#60

#=========================Find Contours=============================
# find contours in the thresholded image
cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
	cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if imutils.is_cv2() else cnts[1]

# Select only largest contours
# Largest contours: c = max(cnts, key=cv2.contourArea)
c = max(cnts, key=cv2.contourArea)
for index, c in enumerate(cnts):
    print "Contour ", index, ": "
    #Generate new img with only the largest found contour
    #filtered = np.zeros(image.shape, np.uint8)
    #cv2.drawContours(filtered, [c], -1, (0, 255, 0), 1)
    findArrow(c)




#=========================Find HoughLines=============================
# thetaList = []
# filteredLineIndex = []

#gray = cv2.cvtColor(filtered,cv2.COLOR_BGR2GRAY)
#edges = cv2.Canny(gray,50,150,apertureSize = 3)
# lines = cv2.HoughLines(edges,1,np.pi/180,50)
# print len(lines)
#
# def isSimilarLine(potentialTheata):
#     for count, theta in enumerate(thetaList):
#         if (abs(theta - potentialTheata) < 0.1):
#             return True
#     return False
#
# for index, line in enumerate(lines):
#
#     for rho,theta in line:
#         if(isSimilarLine(theta) == False):
#             filteredLineIndex.append(index)
#             thetaList.append(theta)
# print thetaList
# print filteredLineIndex
#
#
# for index in filteredLineIndex:
#     currentLine = lines[index]
#     rho, theta = currentLine[0]
#
#     a = np.cos(theta)
#     b = np.sin(theta)
#     x0 = a*rho
#     y0 = b*rho
#     x1 = int(x0 + 1000*(-b))
#     y1 = int(y0 + 1000*(a))
#     x2 = int(x0 - 1000*(-b))
#     y2 = int(y0 - 1000*(a))
#
#     cv2.line(image,(x1,y1),(x2,y2),(0,0,255),2)

#==================================End of find HoughLines========================


