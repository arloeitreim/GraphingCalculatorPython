from Graph import Graph
from Calculator import Calculator
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtCore import Qt, QPoint, QLineF
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import (QWidget, QPushButton, QLabel, QHBoxLayout, QSlider, QMenuBar)
from PyQt5.QtGui import QFont
import sys
import PyQt5
from Regression import Regression

if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
	PyQt5.QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
	PyQt5.QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)


class RegressionGUI(QWidget):
	def __init__(self):
		super().__init__()
		self.setGeometry(300, 100, 700, 500)

		self.regression = Regression()
		self.regression.setGeometry(500, 100, 500, 500)
		self.regression.setFixedSize(500, 500)

		horizontal_box = QHBoxLayout()
		horizontal_box.setAlignment(QtCore.Qt.AlignLeft)
		horizontal_box.setAlignment(QtCore.Qt.AlignBottom)
		horizontal_box.stretch(1)
		horizontal_box.addWidget(self.regression)

		self.setLayout(horizontal_box)

		header = QFont("Calibre")
		header.setPointSize(14)
		header.setBold(True)

		regression_label = QLabel('Regressions', self)
		regression_label.move(553, 10)
		regression_label.setFont(header)
		regression_label.resize(140, 50)

		linear_button = QPushButton('Linear', self)
		linear_button.move(560, 70)
		linear_button.resize(100, 50)

		exponential_button = QPushButton('Exponential', self)
		exponential_button.move(560, 130)
		exponential_button.resize(100, 50)


if __name__ == '__main__':
	app = QApplication(sys.argv)
	regression_GUI = RegressionGUI()
	regression_GUI.show()

	sys.exit(app.exec_())