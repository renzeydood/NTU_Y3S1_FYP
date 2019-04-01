'''
Notes:
- Modified version of the QGraphicsScene for mouse press events
'''
from PyQt5.QtWidgets import QGraphicsScene
from PyQt5.QtCore import QPointF

class DisplayScene(QGraphicsScene):
    def __init__ (self, parent=None):
        super(DisplayScene, self).__init__ (parent)

    def addBoardObject(self, boardObject):
        self.boardObject = boardObject

    def mousePressEvent(self, event):
        position = QPointF(event.scenePos())
        print("pressed here: " + str(int(position.x()/70)) + ", " + str(int(position.y()/70)))
        self.boardObject.addBlock(int(position.x()/70), int(position.y()/70))
        self.boardObject.getArray()
