from CameraManager import *
import argparse
import imutils
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help = "Path to the image")
args = vars(ap.parse_args())

cam = CameraManager(args["image"])

#cam.displayFiltered()

shapesFound = cam.findShapes()
for shape in shapesFound:
    cam.drawShapes(shape)

cam.displayFrame()

#cam.boundROI()