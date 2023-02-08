from Graph import Graph
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtCore import Qt, QPoint
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication
import sys
import numpy as np
import PyQt5
import math

if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    PyQt5.QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    PyQt5.QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)


def makeQPoint(coordinates):
    return QPoint(*coordinates)


class Regression(Graph):
    def __init__(self):
        super().__init__([], 1, scale_factor=1)
        self.setWindowTitle('Regression')
        self.mode = 'exponential'
        self.setMouseTracking(True)
        self.points = []

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)

        self.draw_axes(qp)
        self.draw_grid(qp)

        qp.scale(self.scaleFactor, self.scaleFactor)

        rgb_values = [[255, 0, 0], [0, 0, 250], [0, 250, 0], [0, 100, 100], [255, 0, 255]]
        colors = dict()

        if self.functions:
            for i, function in enumerate(self.functions):
                colors[function] = QColor(*rgb_values[i], self.opacities[function])
            for function in self.functions:
                self.draw_function(qp, function, colors[function], self.z)

        # Resets the scale
        qp.scale(1 / self.scaleFactor, 1 / self.scaleFactor)

        self.draw_axes_labels(qp, self.zoom)

        self.draw_points(qp)
        qp.end()

    def draw_points(self, qp):
        point_pen = QPen(QColor(30, 30, 255), 5)
        qp.setPen(point_pen)

        for point in self.points:
            qp.drawRoundedRect(*point, 1, 1, 0.1, 0.1)

    def mousePressEvent(self, event):
        check_x: int
        check_y: int
        index: int
        point = event.pos()
        x = point.x()
        y = point.y()
        if event.button() == Qt.LeftButton:
            self.points.append((x, y))

        elif event.button() == Qt.RightButton:
            for i in range(-3, 3):
                for j in range(-3, 3):
                    check_x = x + i
                    check_y = y + j
                    try:
                        index = self.points.index((check_x, check_y))
                        del self.points[index]
                    except ValueError:
                        pass

        if len(self.points) > 1:
            if self.mode == 'exponential':
                self.exponential_regression()
            if self.mode == 'linear':
                self.linear_regression()

        self.update()

    def linear_regression(self):
        m: int
        b: int
        equation: str

        zoom = 1 / self.zoom
        x_list = [point[0] for point in self.points]
        x_list = np.subtract(x_list, 250)
        x_list = np.dot(x_list, zoom)
        x_list = np.dot(x_list, self.scaleFactor)

        y_list = [point[1] for point in self.points]
        y_list = np.dot(y_list, zoom)
        y_list = np.dot(y_list, self.scaleFactor)
        y_list = np.dot(y_list, -1)
        y_list = np.add(y_list, 10)

        x_squared_list = [x ** 2 for x in x_list]
        x_times_y_list = np.multiply(x_list, y_list)
        number_of_points = len(x_list)
        m = (number_of_points * sum(x_times_y_list) - sum(x_list) * sum(y_list)) / (
                    number_of_points * sum(x_squared_list) - (sum(x_list) ** 2))
        b = (sum(y_list) - m * sum(x_list)) / number_of_points

        equation = f'{m: .5}x + {b: .5}'
        equation = equation.replace('  ', ' ')

        print(equation)

        # clears function list to prevent overlapping functions
        self.functions = []

        self.functions.append(equation)
        self.opacities[equation] = 250

        self.update()

    def exponential_regression(self):
        a: int
        b: int
        equation: str

        zoom = 1 / self.zoom

        x_list = [point[0] for point in self.points]
        x_list = np.subtract(x_list, 250)
        x_list = np.dot(x_list, zoom)
        x_list = np.dot(x_list, self.scaleFactor)

        y_list = [point[1] for point in self.points]
        y_list = np.subtract(y_list, 250)
        y_list = np.dot(y_list, zoom)
        y_list = np.dot(y_list, self.scaleFactor)
        y_list = np.dot(y_list, -1)

        balancer = 0
        for i, y in enumerate(y_list):
            if y <= 0:
                i -= balancer

                y_list = np.delete(y_list, i)
                x_list = np.delete(x_list, i)

                balancer += 1

        y_list = list(map(math.log, y_list))

        x_squared_list = [x ** 2 for x in x_list]

        x_times_y_list = np.multiply(x_list, y_list)

        number_of_points = len(x_list)

        a = (sum(y_list) * sum(x_squared_list) - sum(x_list) * sum(x_times_y_list)) / (
                number_of_points * sum(x_squared_list) - (sum(x_list) ** 2))

        b = (number_of_points * sum(x_times_y_list) - sum(x_list) * sum(y_list)) / (
                    number_of_points * sum(x_squared_list) - (sum(x_list) ** 2))

        equation = f' ( {math.e} ^ {a: .5} ) {math.e} ^ ( {b: .5} * x ) '
        equation = equation.replace('  ', ' ')

        print(equation)

        # clears function list to prevent overlapping functions
        self.functions = []

        self.functions.append(equation)
        self.opacities[equation] = 250

        self.update()

    def change_mode(self, mode):
        self.mode = mode
        if len(self.points) > 1:
            self.functions = []
            if self.mode == 'exponential':
                self.exponential_regression()
            if self.mode == 'linear':
                self.linear_regression()
        self.update()

    def clear_points(self):
        self.points = []
        self.functions = []
        self.update()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    regression = Regression()
    regression.show()

    sys.exit(app.exec_())
