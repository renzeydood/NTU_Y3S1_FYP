# import the necessary packages

import imutils
import cv2
import time
import numpy as np
import math
from picamera.array import PiRGBArray
from picamera import PiCamera

def drawShapes(c, label, labelLocation):
    cv2.drawContours(image, [c], -1, (0, 255, 0), 3)
    cv2.putText(image, label, (labelLocation[0] - 50, labelLocation[1] - 50),
    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255) , 1)


def checkInRange(value, lower, upper):
    if lower <= value <= upper :
        return True
    return False

def angleToTipOrientation(anglePair):

    tolerance = 10;
    #print "anglepair: ", anglePair[0], " ", anglePair[1]
    #print "checkInRange(anglePair[0], -(45+tolerance), -(45-tolerance)): ", checkInRange(anglePair[0], -(45+tolerance), -(45-tolerance))
    #print "checkInRange(anglePair[1], -(135+tolerance), -(135-tolerance))", checkInRange(anglePair[1], -(135+tolerance), -(135-tolerance))

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
def findArrow(c, approx):
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
            tipOrientation = angleToTipOrientation((angle1,angle2))
            potentialArrowOrient = potentialArrowOrient if tipOrientation == None else tipOrientation
            ptAngle = abs(angle1 + angle2)
            # print "Angle1: ", angle1
            # print "Angle2: ", angle2
            # print "Combine angle: ", ptAngle

            if abs(ptAngle) < 25 or abs(ptAngle - 90) < 25 or abs(ptAngle - 180) < 25 or abs(ptAngle - 270) < 25 :
                rightAngleCounter+=1


            #cv2.putText(filtered, str(m), (m[0][0], m[0][1]),
            #cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255) , 1)

    if(rightAngleCounter == 5 and potentialArrowOrient != None):
        print "ARROW DETECTED"
        print potentialArrowOrient

        drawShapes(c, potentialArrowOrient, approx[0][0])

def findShapes(c):

    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.04 * peri, True)#0.04
    length = len(approx)
    if( length == 7):
        findArrow(c, approx)
    # elif(length == 3 and cv2.contourArea(c) > 200):
        # drawShapes(c, "Triangle", approx[0][0])
    # elif(length == 0 and cv2.contourArea(c) > 200):
        # drawShapes(c, "Circle", approx[0][0])



#===================================================================================================================

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera)

# allow the camera to warmup
#time.sleep(0.1)

# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	# grab the raw NumPy array representing the image, then initialize the timestamp
	# and occupied/unoccupied text
    image = frame.array
    # load the image, convert it to grayscale, blur it slightly,
    # and threshold it
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY_INV)[1]#60

    # find contours in the thresholded image
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if imutils.is_cv2() else cnts[1]
    c = max(cnts, key=cv2.contourArea)
    for index, c in enumerate(cnts):
        print "Contour ", index, ": ", c
        print "c[0][0][0]:    ", c[0][0][0]
        findShapes(c)

    cv2.imshow("Arrow", image)
    key = cv2.waitKey(1) & 0xFF

	# clear the stream in preparation for the next frame
    rawCapture.truncate(0)

	# if the `q` key was pressed, break from the loop
    if key == ord("q"):
		break
