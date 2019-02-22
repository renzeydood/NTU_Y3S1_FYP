class Shapes():

    #Entity class which is use to keep track of Shapes object identified by the
    #camera.

    def __init__(self, type, contour, orientation = None):

        #e.g Arrow, triangle, circle...
        self.type = type
        #Contour data of the shape()
        self.contour = contour
        #Orientation of shape if exist. Default to None.
        self.orientation = orientation

    def getType(self):
        return self.type

    def getContour(self):
        return self.contour

    def getOrientation(self):
        return self.orientation
