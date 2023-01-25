import PyQt5
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QPushButton, QLabel, QHBoxLayout, QSlider, QAbstractSlider)
from PyQt5.QtGui import QFont

from Graph import Graph

import sys

if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
	PyQt5.QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
	PyQt5.QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)


class GraphGUI(QWidget):
	def __init__(self, functions):
		super().__init__()
		self.setGeometry(500, 100, 700, 500)

		self.functions = functions

		self.__init__GUI()
		self.__init__Graph()
		self.connect_buttons()

	def __init__GUI(self):
		self.zoom = 1

		header = QFont("Calibre")
		header.setPointSize(14)
		header.setBold(True)


		font = QFont("Calibre")
		font.setPointSize(16)
		#font.setBold(True)

		self.zoom_label = QLabel('Zoom', self)
		self.increase = QPushButton('+', self)
		self.decrease = QPushButton('−', self)

		self.zoom_label.setFont(header)
		self.increase.setFont(font)
		self.decrease.setFont(font)

		self.zoom_label.move(585, 20)
		self.increase.move(555, 60)
		self.decrease.move(620, 60)

		self.increase.resize(50, 50)
		self.decrease.resize(50, 50)

		self.transparency_label = QLabel('Transparency', self)
		self.transparency_label.setFont(header)
		self.transparency_label.adjustSize()
		self.transparency_label.move(547, 140)
		function_labels = dict()
		sliders = dict()
		function_buttons = dict()
		for i, function in enumerate(self.functions):
			if i > 4:
				break

			function_labels[function] = QLabel(function, self)
			function_labels[function].setFont(font)
			function_labels[function].move(585, 180 + (i * 80))

			sliders[function] = QSlider(Qt.Horizontal, self)
			sliders[function].setGeometry(560, 220 + (i * 80), 100, 10)
			sliders[function].setSingleStep(100)

			change_opacity = self.change_opacity_closed(function)

			sliders[function].setTracking(False)
			sliders[function].setRange(0, 250)
			sliders[function].setInvertedAppearance(True)
			sliders[function].setValue(250)
			sliders[function].valueChanged[int].connect(change_opacity)

	def __init__Graph(self):
		self.graph = Graph(self.functions, 1)
		self.graph.setGeometry(500, 100, 500, 500)
		self.graph.setFixedSize(500, 500)

		horizontal_box = QHBoxLayout()
		horizontal_box.setAlignment(QtCore.Qt.AlignLeft)
		horizontal_box.stretch(1)
		horizontal_box.addWidget(self.graph)

		self.setLayout(horizontal_box)

	def connect_buttons(self):
		self.increase.clicked.connect(lambda: self.increase_zoom())
		self.decrease.clicked.connect(lambda: self.decrease_zoom())

	def change_opacity_closed(self, function):
		def change_opacity(value):
			print(value)
			self.graph.change_opacity(function, value)
		return change_opacity
		
	def change_value_of_z(self):
		# If Z is present in the function, create a slider to allow the user to adjust the value of z
		pass

	def increase_zoom(self):
		if not self.zoom <= 0:
			self.zoom -= 1
		self.graph.change_zoom(self.zoom)

	def decrease_zoom(self):
		if not self.zoom >= 4:
			self.zoom += 1
		self.graph.change_zoom(self.zoom)


if __name__ == '__main__':
	app = QtWidgets.QApplication([])
	functions = ['2 ^ x', 'x ^ 2']
	graph_GUI = GraphGUI(functions)
	graph_GUI.show()
	sys.exit(app.exec_())
