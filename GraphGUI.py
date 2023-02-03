import PyQt5
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QPushButton, QLabel, QHBoxLayout, QSlider, QMenuBar)
from PyQt5.QtGui import QFont
from Graph import Graph
from Calculator import Calculator

import sys

if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
	PyQt5.QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
	PyQt5.QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)


class GraphGUI(QWidget):
	def __init__(self, functions):
		super().__init__()
		self.setGeometry(300, 100, 865, 540)
		self.setObjectName('GraphGUI')
		self.functions = functions
		self.sliders = dict()
		self.old_z_value: str = '1'

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

		self.zoom_label = QLabel('Zoom', self)
		self.increase = QPushButton('+', self)
		self.decrease = QPushButton('−', self)

		self.zoom_label.setFont(header)
		self.increase.setFont(font)
		self.decrease.setFont(font)

		self.zoom_label.move(585, 30)
		self.increase.move(555, 70)
		self.decrease.move(620, 70)

		self.increase.resize(50, 50)
		self.decrease.resize(50, 50)

		self.header = QLabel('Transparency', self)
		self.header.setFont(header)
		self.header.adjustSize()
		self.header.move(647, 150)

		self.menubar = QtWidgets.QMenuBar(self)
		self.menubar.setGeometry(QtCore.QRect(0, 0, 900, 22))
		self.menubar.setObjectName("menubar")

		self.transparency_action = QtWidgets.QAction(self)
		self.transparency_action.setText('Transparency')
		self.menubar.addAction(self.transparency_action)

		self.z_axis_label = QLabel('Z-Axis', self)
		self.z_axis_label.move(745, 30)
		self.z_axis_label.setFont(header)

		self.z_axis_slider = QSlider(Qt.Horizontal, self)
		self.z_axis_slider.setGeometry(720, 80, 110, 15)
		self.z_axis_slider.setRange(0, 500)
		self.z_axis_slider.setValue(250)

		function_labels = dict()
		self.sliders = dict()

		for i, function in enumerate(self.functions):
			if i > 4:
				break

			without_html = Calculator.translate(function)
			without_html = without_html.replace(' (', '')
			without_html = without_html.replace(') ', '')

			font.setPointSizeF(14 - (len(without_html) / 4))

			function_labels[function] = QLabel(function, self)
			function_labels[function].setFont(font)
			function_labels[function].setWordWrap(True)
			function_labels[function].move(575, 190 + (i * 80))

			self.sliders[function] = QSlider(Qt.Horizontal, self)
			self.sliders[function].setGeometry(560, 230 + (i * 80), 100, 10)
			self.sliders[function].setSingleStep(100)

			change_opacity = self.change_opacity_closed(function)

			self.sliders[function].setRange(0, 250)
			self.sliders[function].setInvertedAppearance(True)
			self.sliders[function].setValue(250)
			self.sliders[function].valueChanged[int].connect(change_opacity)

	def __init__Graph(self):
		self.graph = Graph(self.functions, 1)
		self.graph.setGeometry(500, 100, 500, 500)
		self.graph.setFixedSize(500, 500)

		horizontal_box = QHBoxLayout()
		horizontal_box.setAlignment(QtCore.Qt.AlignLeft)
		horizontal_box.setAlignment(QtCore.Qt.AlignBottom)
		horizontal_box.stretch(1)
		horizontal_box.addWidget(self.graph)

		self.setLayout(horizontal_box)

	def connect_buttons(self):
		self.increase.clicked.connect(lambda: self.increase_zoom())
		self.decrease.clicked.connect(lambda: self.decrease_zoom())
		self.transparency_action.triggered.connect(lambda: self.change_header_and_connection('Transparency', self.change_opacity_closed))
		self.z_axis_slider.valueChanged[int].connect(self.change_z_axis)

	def change_z_axis(self,   value):
		value = str((value * -1 + 250) / 100)
		self.graph.change_z_axis(value)

	#def make_transparency_visible(self):
		#self.transparency

	def change_opacity_closed(self, function):
		def change_opacity(value):
			self.graph.change_opacity(function, value)
		return change_opacity

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
	#functions = ['2 ^ x', 'x ^ 2 - 0.2', 'x <sup> 3 </sup>', '√ x']
	#functions = ['x * z ^ 3 - z * x ^ 3']
	functions = ['-1 ÷ ( x ^ 2 + z ^ 2 ) ', 'x * z ^ 3 - z * x ^ 3', ' ( x ^ 4 ) ÷ ( z ^ 3 ) ']
	graph_GUI = GraphGUI(functions)
	graph_GUI.show()
	sys.exit(app.exec_())
