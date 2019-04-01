import imutils
import cv2

image = cv2.imread("jp.jpg")

(h, w, d) = image.shape #Get size and colour channels of the image
print("width={}, height={}, depth={}".format(w, h, d))

(b, g, r) = image[100, 50] #Get intensity value of the 3 color channels
print("R={}, G={}, B={}".format(r,g,b))

""" roi = image[60:160, 320:420]
cv2.imshow("Region Of Interest", roi) """

""" rh = 300.0 / w  #Ratio based on width
newdim = (300, int(h * rh))
resized = cv2.resize(image, newdim)
#Or use imutils library, better
resized = imutils.resize(image, width=300)
cv2.imshow("Aspect Ratio Resize", resized)"""

""" center = (w//2, h//2)
M = cv2.getRotationMatrix2D(center, -45, 1.0)
rotated = cv2.warpAffine(image, M, (w,h))
#Or use imutils library
#rotated = imutils.rotate(image, -45)
rotated = imutils.rotate_bound(image, 45) #Enlarge bounds to preserve all pixels
cv2.imshow("OpenCV Rotation", rotated) """

""" blurred = cv2.GaussianBlur(image, (11,11), 0)
cv2.imshow("Blurred", blurred) """

output = image.copy() #Draw from a copy of the image
cv2.rectangle(output, (320, 60), (420, 160), (0, 0, 255), 2 ) #Starting pixel(top-left), ending pixel(bottom-right), color(BGR), line width
cv2.circle(output, (300, 150), 20, (255, 0, 0), -1) #Start point, radius, colour, line thickness (-1 = filled)
cv2.line(output, (60, 20), (400, 200), (0, 255, 0), 5)
cv2.putText(output, "OpenCV + Jurrassic Park!!!", (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2) #tex, starting point, font, scale, colour, thickness
cv2.imshow("Text", output)

#cv2.imshow("Image", image)
cv2.waitKey(0)