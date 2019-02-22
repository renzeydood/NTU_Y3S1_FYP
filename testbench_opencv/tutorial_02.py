import argparse
import imutils
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="path to input image")
args = vars(ap.parse_args())

image = cv2.imread(args["image"])
""" cv2.imshow("Image", image)
cv2.waitKey(3000) """

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
""" cv2.imshow("Gray", gray)
cv2.waitKey(0) """

""" edged = cv2.Canny(gray, 30, 150)
cv2.imshow("Edged", edged)
cv2.waitKey(0) """

thresh = cv2.threshold(gray, 225, 255, cv2.THRESH_BINARY_INV)[1]
""" cv2.imshow("Thresh", thresh)
cv2.waitKey(0) """

""" cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
output = image.copy()

print(len(cnts)) #returns the number of contours found
for c in cnts:
    cv2.drawContours(output, [c], -1, (240, 0, 159), 3)
    cv2.imshow("Contours", output)
    cv2.waitKey(0) """

""" mask = thresh.copy()
mask = cv2.erode(mask, None, iterations=5) #Reduce noise from thresholding by eroding image 5 times, it makes the foreground smaller
cv2.imshow("Eroded", mask)
cv2.waitKey(0) """

""" mask = thresh.copy()
mask = cv2.dilate(mask, None, iterations=5) #Reverse of eroding, makes foreground bigger
cv2.imshow("Dilated", mask)
cv2.waitKey(0) """

""" mask = thresh.copy()
output = cv2.bitwise_and(image, image, mask=mask) #remove background by using bitwise_and on the orignal image and mask
cv2.imshow("Output", output)
cv2.waitKey(0) """

