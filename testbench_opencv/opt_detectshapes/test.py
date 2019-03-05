from colordetector import ColorDetector
import argparse
import imutils
import cv2
import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help = "Path to the image")
args = vars(ap.parse_args())

image = cv2.imread(args["image"])
""" resized = imutils.resize(image, width=300) #Smaller image makes it better to approximate
ratio = image.shape[0] / float(resized.shape[0]) """

imageLAB = cv2.cvtColor(image, cv2.COLOR_RGB2LAB)

redfilterBGR = [199, 108, 112] #[112, 108, 199]  #[66, 48, 182]
greenfilterBGR = [134, 175, 132]
yellowfilterBGR = [117, 255, 255]
thresh = 30

bgr = greenfilterBGR

lab = cv2.cvtColor(np.uint8([[bgr]]), cv2.COLOR_BGR2LAB)[0][0]
 
minLAB = np.array([lab[0] - thresh, lab[1] - thresh, lab[2] - thresh])
maxLAB = np.array([lab[0] + thresh, lab[1] + thresh, lab[2] + thresh])

maskLAB = cv2.inRange(imageLAB, minLAB, maxLAB)
#resultLAB = cv2.bitwise_and(image, image, mask=maskLAB)
cv2.imshow("Result BGR", maskLAB)

cnts = cnts = cv2.findContours(maskLAB, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
output = image.copy()

print(len(cnts)) #returns the number of contours found
for c in cnts:
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.04 * peri, True)#0.04
    line = len(approx)
    
    if cv2.contourArea(c) > 3000 and cv2.contourArea(c) < 10000:
        print("Area of contour: ", cv2.contourArea(c), "Length: ", line)
        cv2.drawContours(output, [c], -1, (240, 0, 159), 2)
        cv2.imshow("Contours", output)
        cv2.waitKey(0)

cv2.waitKey(0)