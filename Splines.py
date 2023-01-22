from PyQt5.QtGui import QPainter, QPen, QBrush, QPainterPath, QPixmap
from PyQt5 import QtCore, QtGui, uic, QtWidgets
from PyQt5.QtWidgets import QWidget, QGraphicsScene, QGraphicsPixmapItem, QStyleOptionGraphicsItem, QGraphicsView, QGraphicsPathItem, QGraphicsLineItem, QGraphicsItem, QGraphicsRectItem, QGraphicsEllipseItem, QApplication
from PyQt5.QtCore import Qt, QPointF, QPoint
import PyQt5
import PySide2
import sys

if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    PyQt5.QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    PyQt5.QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

qp = QPainter()


app = QApplication(sys.argv)
scene = QGraphicsScene(0, 0, 400, 200)


points = [QPoint(10, 100), QPoint(110, 50), QPoint(210, 100)]
pix = QPixmap(points[0].x(), points[0].y())

#line = QGraphicsLineItem(points[0].x(), points[0].y(), points[1].x(), points[1].y())
line = QGraphicsLineItem(10, 10, 10, 10)
line2 = QGraphicsLineItem(points[1].x(), points[1].y(), points[2].x(), points[2].y())

pen = QPen(Qt.darkRed)
pen.setWidth(3)
qp.setPen(pen)



line.setPen(pen)
#line.setGraphicsEffect()
line2.setPen(pen)


map = QGraphicsPixmapItem(pix)

#scene.addItem(line)
#scene.addItem(line2)
scene.addItem(map)

line.setFlag(QGraphicsItem.ItemIsMovable)
line2.setFlag(QGraphicsItem.ItemIsMovable)

view = QGraphicsView(scene)
view.setRenderHint(QPainter.Antialiasing, True)
view.setRenderHint(QPainter.SmoothPixmapTransform, True)
view.setRenderHint(QPainter.HighQualityAntialiasing, True)
view.show()
app.exec_()

