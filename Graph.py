from Calculator import Calculator
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtCore import Qt, QPointF, QLineF
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QFont
import sys
import PyQt5
from math import isinf
import logging
from functools import cache


if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
	PyQt5.QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
	PyQt5.QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

class Graph(QWidget):
    def __init__(self, functions, zoom):
        super().__init__()

        self.minor_grid = True
        self.zoom = self.__get_zoom(zoom)
        self.scaleFactor = 0.1
        self.opacities = dict()


        if type(functions) is str:
            self.functions = [functions]
        else:
            self.functions = functions

        for function in self.functions:
            self.opacities[function] = 250

        self.setGeometry(500, 100, 500, 500)
        self.setWindowTitle("Graph")


    def __get_zoom(self, zoom):
        if zoom < 0:
            self.minor_grid = True
            return 50

        elif zoom == 0:
            self.minor_grid = True
            return 50

        elif zoom == 1:
            self.minor_grid = True
            return 25

        elif zoom == 2:
            self.minor_grid = True
            return 10

        elif zoom == 3:
            self.minor_grid = False
            return 5

        elif zoom == 4:
            self.minor_grid = False
            return 1

        elif zoom > 4:
            self.minor_grid = False
            return 1


    def change_zoom(self, zoom):
        self.zoom = self.__get_zoom(zoom)
        self.update()

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)

        self.draw_axes(qp)
        self.draw_grid(qp)

        qp.scale(self.scaleFactor, self.scaleFactor)

        rgb_values = [[255, 0, 0], [0, 0, 250], [0, 250, 0], [0, 100, 100], [255, 0, 255]]

        colors = dict()

        for i, function in enumerate(self.functions):
            colors[function] = QColor(*rgb_values[i], self.opacities[function])

        for function in self.functions:
            self.draw_function(qp, function, colors[function])

        # Resets the scale
        qp.scale(1 / self.scaleFactor, 1 / self.scaleFactor)

        self.draw_axes_labels(qp)

        qp.end()

    def draw_axes(self, qp):

        horizontal_spacing: int
        vertical_spacing: int

        axes = QColor(0, 0, 0, 150)
        axes_pen = QPen(axes, 2, Qt.SolidLine)

        qp.setPen(axes_pen)
        qp.drawLine(0, 250, 500, 250)
        qp.drawLine(250, 0, 250, 500)


    def draw_axes_labels(self, qp):
        # if the class instance zoom is not greater than 25, set it to 10
        # this makes sure the labels don't get too clumped together when the graph is very zoomed out
        if self.zoom >= 25:
            zoom = self.zoom
        else:
            zoom = 10

        axes = QColor(0, 0, 0, 150)
        axes_pen = QPen(axes, 2, Qt.SolidLine)
        qp.setPen(axes_pen)

        font = QFont()
        font.setBold(True)
        font.setFixedPitch(True)
        font.setPointSize(self.__get_point_size())
        qp.setFont(font)

        # draws the zero label for both the x-axis and y-axis
        qp.drawText(242, 260, '0')

        # Draws the x-coordinate labels every major line
        for x in range(-250 + zoom * 5, 249, zoom * 5):
            x_label = int(x / self.zoom)

            horizontal_spacing = self.__get_horizontal_spacing(x_label)
            vertical_spacing = 5 - self.__get_point_size()

            x_label = str(x_label)

            if not x == 0:
                qp.drawText(x + 252 - horizontal_spacing, 260 - vertical_spacing, x_label)

        # Draws the y-coordinate labels every major line
        for y in range(-250 + zoom * 5, 250, zoom * 5):
            y_label = int(-y / self.zoom)

            horizontal_spacing = self.__get_horizontal_spacing(y_label)

            y_label = str(y_label)

            if y != 0:
                qp.drawText(245 - horizontal_spacing, y + 253, y_label)


    def __get_point_size(self):
        match self.zoom:
            case 50:
                return 8

            case 25:
                return 7

            case 10:
                return 6

            case 5:
                return 5

            case 1:
                return 5


    def __get_horizontal_spacing(self, coordinate):
        spacing: int
        length = len(str(coordinate))
        spacing = self.__get_point_size() * 0.65 * length

        return int(spacing)


    def draw_grid(self, qp):
        if self.zoom >= 25:
            zoom = self.zoom

        else:
            zoom = 10

        major_grid = QColor(0, 0, 0, 50)
        minor_grid = QColor(0, 0, 0, 20)
        major_grid_pen = QPen(major_grid, 1, Qt.SolidLine)
        minor_grid_pen = QPen(minor_grid, 1, Qt.SolidLine)

        qp.setPen(major_grid_pen)

        # Draws a major horizontal lines every few minor lines
        for x in range(0, 501, zoom * 5):
            qp.drawLine(x, 0, x, 500)

        # Draws a major horizontal lines every few minor lines
        for y in range(0, 501, zoom * 5):
            qp.drawLine(0, y, 500, y)

        # Only draws the minor lines if the zoom level is below 2
        if self.minor_grid:
            qp.setPen(minor_grid_pen)

            # Draws minor horizontal lines in increments of the zoom instance variable
            for x in range(0, 501, self.zoom):
                qp.drawLine(x, 0, x, 500)

            # Draws minor horizontal lines in increments of the zoom instance variable
            for y in range(0, 501, self.zoom):
                qp.drawLine(0, y, 500, y)

    def draw_function(self, qp, function, color):
        pen = QPen(color, 7, Qt.SolidLine, Qt.RoundCap)
        pen.setJoinStyle(Qt.RoundJoin)
        pen.setCosmetic(True)
        qp.setPen(pen)
        #qp.setCompositionMode(QPainter.CompositionMode_DestinationOut)
        qp.setRenderHint(QPainter.SmoothPixmapTransform, True)
        qp.setRenderHint(QPainter.Antialiasing, True)

        lines, points = self.get_lines(function, self.zoom)

        qp.drawPoints(points)
        qp.drawLines(lines)

    @cache
    def get_lines(self, function: str, zoom):
        continuous = False
        point1: QPointF
        point2: QPointF
        points: list = []
        lines: list = []
        line: QLineF
        calculator = Calculator()

        get_point = self.get_point(function)
        start = int(-250 / self.scaleFactor)
        end = int(250 / self.scaleFactor)

        for x in range(start, end):
            try:
                point2 = get_point(x)

                if not continuous:
                    points.append(point2)

                elif continuous:
                    line = QLineF(point1, point2)
                    lines.append(line)

                point1 = point2

                continuous = True

            except ValueError:
                continuous = False

        return (lines, points)


    def get_point(self, function):
        calculator = Calculator()

        def get_point_inner(x):
            y: float

            # adjusts x for the scale and zoom of the graph
            x = (x * self.scaleFactor
                 / self.zoom)

            # Calculates y-value
            y = float(
                calculator.PEMDAS
                (function.replace('x', ' ( ' + str(x) + ' ) ')))

            logging.info(f'x: {x} \n y: {y}')

            # checks if y is a complex number or infinite
            self.check_complex(y)
            #self.check_infinity(y)

            # map y on to the graph
            y = y / self.scaleFactor \
                * -1\
                * self.zoom \
                + 250 / self.scaleFactor

            # map x onto the graph
            x = (x / self.scaleFactor
                 * self.zoom
                 + int(250 / self.scaleFactor))

            point = QPointF(x, y)

            return point

        return get_point_inner

    def change_opacity(self, function, opacity_level):
        self.opacities[function] = opacity_level
        self.update()


    def check_complex(self, y_float):
        if 'j' in str(y_float):
            # 'e' in str(y_float) or 'j' in str(y_float):
            print('imaginary: ' + y_float)
            raise ValueError


    def check_infinity(self, y_float):
        if isinf(y_float):
            print('infinity')
            raise ValueError


if __name__ == '__main__':
    #logging.basicConfig(level=logging.INFO)
    app = QApplication(sys.argv)
    functions = ['√ ( x ) - 5']
    graph = Graph(functions, 1)
    graph.show()

    sys.exit(app.exec_())
