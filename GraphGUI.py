import PyQt5
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5.QtWidgets import (QWidget, QPushButton, QLabel, QHBoxLayout)
from PyQt5.QtGui import QFont

from Graph import Graph

import sys

if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
	PyQt5.QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
	PyQt5.QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)


class GraphGUI(QWidget):
	def __init__(self):
		super().__init__()
		self.zoom = 1
		self.setGeometry(500, 100, 700, 500)
		self.graph = Graph('x ^ 2', 1)
		self.graph.setGeometry(500, 100, 500, 500)
		self.graph.setFixedSize(500, 500)
		self.zoom_label = QLabel('Zoom', self)
		self.increase = QPushButton('+', self)
		self.decrease = QPushButton('−', self)
		font = QFont("Calibri")
		font.setPointSize(16)
		font.setBold(True)
		self.zoom_label.setFont(font)
		self.increase.setFont(font)
		self.decrease.setFont(font)
		self.zoom_label.move(585, 30)
		self.increase.move(570, 60)
		self.increase.resize(40, 40)
		self.decrease.move(615, 60)
		self.decrease.resize(40, 40)

		hbox = QHBoxLayout()
		hbox.setAlignment(QtCore.Qt.AlignLeft)
		hbox.stretch(1)
		hbox.addWidget(self.graph)

		self.setLayout(hbox)

		self.increase.clicked.connect(lambda: self.increase_zoom())
		self.decrease.clicked.connect(lambda: self.decrease_zoom())

	def increase_zoom(self):
		if not self.zoom >= 4:
			self.zoom += 1
		self.graph.change_zoom(self.zoom)

	def decrease_zoom(self):
		if not self.zoom <= 0:
			self.zoom -= 1
		self.graph.change_zoom(self.zoom)




if __name__ == '__main__':
	app = QtWidgets.QApplication([])
	graph_GUI = GraphGUI()
	graph_GUI.show()
	sys.exit(app.exec_())
