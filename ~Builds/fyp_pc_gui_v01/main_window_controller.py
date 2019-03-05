import sys
import time	
from displayScene import DisplayScene
from robot import Robot
from board import Board
from PyQt5 import QtGui, uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QDesktopWidget, QGraphicsScene, QGraphicsView, QGraphicsEllipseItem, QLabel, QGraphicsPixmapItem, QGraphicsItem
from PyQt5.QtGui import QBrush, QPen, QPixmap, QTransform
from PyQt5.QtCore import Qt, pyqtSlot, QRectF, QPointF, QSizeF, QObject

class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        uic.loadUi('main_window_ui.ui', self)
        
        self.btn_Start.clicked.connect(self.btn_Start_Clicked)
        self.btn_Reset.clicked.connect(self.btn_Reset_Clicked)
        self.btn_Up.clicked.connect(self.btn_Up_Clicked)
        self.btn_Down.clicked.connect(self.btn_Down_Clicked)
        self.btn_Left.clicked.connect(self.btn_Left_Clicked)
        self.btn_Right.clicked.connect(self.btn_Right_Clicked)

        self.MapInit()
        self.InitWindow()
    #end

    def MapInit(self):
        self.scene = DisplayScene()


        self.scene.setSceneRect(0, 0, 500, 500)


        self.view_Map.setScene(self.scene)
    #end

    def InitWindow(self):
        #self.setGeometry(self.top, self.left, self.width, self.height)
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        self.setWindowTitle('Center')
        self.show()
    #end

    def btn_Down_Clicked(self):
        self.tBox_Logs.append("Move backward")
    #end

    def btn_Up_Clicked(self):
        self.tBox_Logs.append("Move forward")
    #end

    def btn_Left_Clicked(self):
        self.tBox_Logs.append("Turn left")
    #end

    def btn_Right_Clicked(self):
        self.tBox_Logs.append("Turn right")
    #end

    def btn_Start_Clicked(self):
        self.tBox_Logs.append("Exploration Start")
    #end

    def btn_Reset_Clicked(self):
        self.tBox_Logs.clear()
        self.update()
    #end

    #def onClick(self, event):
    #    items = self.scene().items(event.scenePos())

App = QApplication(sys.argv)
window = Window()
sys.exit(App.exec())