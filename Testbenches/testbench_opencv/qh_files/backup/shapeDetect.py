# import the necessary packages
import argparse
import imutils
import cv2
import time
import numpy as np
from picamera.array import PiRGBArray
from picamera import PiCamera


# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
	help="path to the input image")
args = vars(ap.parse_args())

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
rawCapture = PiRGBArray(camera)
# allow the camera to warmup
time.sleep(0.1)
 
# grab an image from the camera
camera.capture(rawCapture, format="bgr")
image = rawCapture.array

# load the image, convert it to grayscale, blur it slightly,
# and threshold it
#image = cv2.imread(args["image"])
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY_INV)[1]#60



cv2.imshow("thresh", thresh)
cv2.waitKey(0)

# find contours in the thresholded image
cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
	cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if imutils.is_cv2() else cnts[1]

# loop over the contours
# Largest contours: c = max(cnts, key=cv2.contourArea)
c = max(cnts, key=cv2.contourArea)
print len(c)
M = cv2.moments(c)
print M["m10"], M["m00"]
if int(M["m00"])  != 0:
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])
        
    # draw the contour and center of the shape on the image
    cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
    peri = cv2.arcLength(c, True)
    print "Peri: ", peri
    approx = cv2.approxPolyDP(c, 0.04 * peri, True)#0.04
    print "len(approx): ", len(approx)
           
        
    for m in approx:
        print m
        cv2.putText(image, str(m), (m[0][0], m[0][1]),
        cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 0, 0), 2)
    print "np.max: ", (np.amax(approx, axis=0))
    print "np.min: ", (np.amin(approx, axis=0))
    # # show the image
    cv2.imshow("Image", image)
    cv2.waitKey(0)
    



# for c in cnts:
    # # compute the center of the contour
    # M = cv2.moments(c)
    # print M["m10"], M["m00"]
    # if int(M["m00"])  != 0:
        # cX = int(M["m10"] / M["m00"])
        # cY = int(M["m01"] / M["m00"])
        
        # # draw the contour and center of the shape on the image
        # cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
        # #cv2.circle(image, (cX, cY), 7, (255, 255, 255), -1)
        # #cv2.putText(image, "center", (cX - 20, cY - 20),
            # #cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        # peri = cv2.arcLength(c, True)
        # approx = cv2.approxPolyDP(c, 0.04 * peri, True)
        # print "len(approx): ", len(approx)
           
        
        # for m in approx:
            # print m
            # cv2.putText(image, str(m), (m[0][0], m[0][1]),
            # cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 0, 0), 2)
        # print "np.max: ", (np.amax(approx, axis=0))
        # print "np.min: ", (np.amin(approx, axis=0))
        # # # show the image
        # cv2.imshow("Image", image)
        # cv2.waitKey(0)