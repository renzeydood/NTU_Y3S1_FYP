import cv2
import numpy as np
from picamera.array import PiRGBArray
from picamera import PiCamera
import time

def isSimilarLine(potentialTheata):
    for count, theta in enumerate(thetaList):
        if (abs(theta - potentialTheata) < 0.1):
            return True
    return False   

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
rawCapture = PiRGBArray(camera)
# allow the camera to warmup
time.sleep(0.1)
 
# grab an image from the camera
camera.capture(rawCapture, format="bgr")
img = rawCapture.array


thetaList = []
filteredLineIndex = []
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray,50,150,apertureSize = 3)

cv2.imshow("edges", edges)
cv2.waitKey(0)

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
edges = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY_INV)[1]#60
cv2.imshow("edges", edges)
cv2.waitKey(0)


lines = cv2.HoughLines(edges,1,np.pi/180,50)

print len(lines)
for index, line in enumerate(lines):

    for rho,theta in line:
        if(isSimilarLine(theta) == False):
            filteredLineIndex.append(index)
            thetaList.append(theta)
print thetaList 
print filteredLineIndex
         

for index in filteredLineIndex:
    currentLine = lines[index]
    rho, theta = currentLine[0]
    
    a = np.cos(theta)
    b = np.sin(theta)
    x0 = a*rho
    y0 = b*rho
    x1 = int(x0 + 1000*(-b))
    y1 = int(y0 + 1000*(a))
    x2 = int(x0 - 1000*(-b))
    y2 = int(y0 - 1000*(a))

    cv2.line(img,(x1,y1),(x2,y2),(0,0,255),2)
    
                   

cv2.imshow("Image", img)
cv2.waitKey(0)

     
            
            
            