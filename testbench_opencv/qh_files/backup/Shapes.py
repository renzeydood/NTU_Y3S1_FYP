class Shapes():

    def __init__(self, type, contour, orientation = None):
        self.type = type
        self.contour = contour
        self.orientation = orientation

    def getType(self):
        return self.type

    def getContour(self):
        return self.contour

    def getOrientation(self):
        return self.orientation
