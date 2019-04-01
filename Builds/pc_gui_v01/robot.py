from PyQt5.QtGui import QPixmap, QTransform
from PyQt5.QtWidgets import QGraphicsScene

class Robot():
    def __init__(self, scene, width, height, xPos = 0, yPos = 1190, blockSize = 70):
        self.blockSize = blockSize
        self.width = blockSize * width
        self.height = blockSize * height
        self.orientation = 0
        self.xPos = xPos
        self.yPos = yPos
        self.transform = QTransform()

        self.robotImg = QPixmap('res/robot_icon_01').scaled(self.blockSize*width, self.blockSize*height)

        self.robotObj = scene.addPixmap(self.robotImg)
        self.robotObj.setPos(xPos, yPos)


    def tryMove(self):
        #This should be in the board class
        pass

    def moveForward(self):
        if self.orientation == 90:
            self.xPos = self.xPos + self.blockSize
        elif self.orientation == 180:
            self.yPos = self.yPos + self.blockSize
        elif self.orientation == 270:
            self.xPos = self.xPos - self.blockSize
        else:
            self.yPos = self.yPos - self.blockSize
        
        self.robotObj.setPos(self.xPos, self.yPos)

    def moveBackward(self):
        if self.orientation == 90:
            self.xPos = self.xPos - self.blockSize
        elif self.orientation == 180:
            self.yPos = self.yPos - self.blockSize
        elif self.orientation == 270:
            self.xPos = self.xPos + self.blockSize
        else:
            self.yPos = self.yPos + self.blockSize
        
        self.robotObj.setPos(self.xPos, self.yPos)

    def rotateRight(self):
        transform = QTransform()

        self.orientation = self.orientation + 90
        if self.orientation == 360:
            self.orientation = 0

        transform.translate(self.width/2.0 , self.width/2.0)
        transform.rotate(self.orientation)
        transform.translate(-self.width/2.0 , -self.width/2.0)
        self.robotObj.setTransform(transform)

    def rotateLeft(self):
        transform = QTransform()

        self.orientation = self.orientation - 90        
        if self.orientation == -90:
            self.orientation = 270

        transform.translate(self.width/2.0 , self.width/2.0)
        transform.rotate(self.orientation)
        transform.translate(-self.width/2.0 , -self.width/2.0)
        self.robotObj.setTransform(transform)
        
    def getPosition(self):
        pass
    
    def getOrientation(self):
        return self.orientation

    def calibrate(self):
        pass

    def deleteRobot(self, scene):
        scene.removeItem(self.robotObj)
