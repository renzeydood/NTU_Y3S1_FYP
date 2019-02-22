'''
Todos: Improve on the grid system's array, maybe use numpy?

Grid legend:
0 = empty
1 = block
2 = robot
3 = start
4 = end
6 = waypoint
7 = arrow
'''

from PyQt5.QtGui import QBrush, QPen
from PyQt5.QtCore import Qt, QRectF, QPointF, QSizeF

class Board():
    def __init__(self, scene, numGridX, numGridY, gridSize = 70, gridColor = 'black'):

        self.gridSize = gridSize
        self.numGridX = numGridX
        self.numGridY = numGridY
        self.scene = scene
        self.gridArray = []
        self.scenePointers = []

        if gridColor == 'red':
            gridLine = QPen(Qt.red)
            gridLine.setWidth(3)
        elif gridColor == 'blue':
            gridLine = QPen(Qt.blue)
            gridLine.setWidth(3)
        elif gridColor == 'green':
            gridLine = QPen(Qt.green)
            gridLine.setWidth(3)
        else:
            gridLine = QPen(Qt.black)
            gridLine.setWidth(3)

        for y in range(numGridY):
            innerArray = []             # x axis
            innerArray2 = []            # x axis
            for x in range(numGridX):
                innerArray.append(0)
                innerArray2.append(0)
                grid = QRectF(QPointF(x*self.gridSize, y*self.gridSize), QSizeF(self.gridSize, self.gridSize))
                self.boardObj = scene.addRect(grid, gridLine)
            self.gridArray.append(innerArray)
            self.scenePointers.append(innerArray2)

    def addBlock(self, setX, setY, color='black'):
        blockColor = QBrush(Qt.black)
        blockOutline = QPen(Qt.black)
        block = QRectF(QPointF(setX*self.gridSize, setY*self.gridSize), QSizeF(self.gridSize, self.gridSize))
        self.scenePointers[setY][setX] = self.scene.addRect(block, blockOutline, blockColor)
        self.gridArray[setY][setX] = 1

    def removeBlock(self, setX, setY):
        if self.gridArray[setX][setY] == 1:
            self.scene.removeItem(self.scenePointers[setX][setY])
            self.scenePointers[setY][setX] = 0
            self.gridArray[setY][setX] = 0

    def initBoard(self):
        #remove the grid here (problems removing grid. need to resolve)
        pass

    def boardBoundary(self):
        pass

    def getArray(self):
        #return self.scenePointers
        #print (self.scenePointers)
        print(self.gridArray)

    def resetGrid(self):
        pass