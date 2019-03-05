import argparse
import imutils
import cv2
from CameraManager import *

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Path to the image")
ap.add_argument("-f", "--filter", help="Display the type of filter to use")
args = vars(ap.parse_args())

cam = CameraManager(args["image"])

cam.displayContours(cam.displayFiltered(args["filter"]))
#cam.displayFiltered(args["filter"])

""" shapesFound = cam.findShapes()
for shape in shapesFound:
    cam.drawShapes(shape)

cam.displayFrame() """

#cam.boundROI()