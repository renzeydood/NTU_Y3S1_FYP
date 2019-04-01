import pyzbar.pyzbar as pyzbar
import numpy as np
import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera

def decode(im) :
  # Find barcodes and QR codes
  decodedObjects = pyzbar.decode(im)

  # Print results
  for obj in decodedObjects:
    print "Type : ", obj.type
    print "Data : ", obj.data, "\n"

  return decodedObjects


# Display barcode and QR code location
def drawQR(im, decodedObjects):

  # Loop over all decoded objects
  for decodedObject in decodedObjects:
    points = decodedObject.polygon

    # If the points do not form a quad, find convex hull
    if len(points) > 4 :
      hull = cv2.convexHull(np.array([point for point in points], dtype=np.float32))
      hull = list(map(tuple, np.squeeze(hull)))
    else :
      hull = points;

    # Number of points in the convex hull
    n = len(hull)

    # Draw the convext hull
    for j in range(0,n):
      cv2.line(im, hull[j], hull[ (j+1) % n], (255,0,0), 3)



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

    drawQR(image, decode(image))

    cv2.imshow("QR", image)
    key = cv2.waitKey(1) & 0xFF

	# clear the stream in preparation for the next frame
    rawCapture.truncate(0)

	# if the `q` key was pressed, break from the loop
    if key == ord("q"):
		break
