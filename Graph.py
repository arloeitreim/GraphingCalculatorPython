import logging
from Calculator import Calculator
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtCore import Qt
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QFont
import sys
import PyQt5
from math import isinf
import logging


class Graph(QWidget):
    def __init__(self, function, zoom):
        super().__init__()
        self.minor_grid = True
        self.zoom = self.__get_zoom(zoom)
        if type(function) is str:
            print('True')
            self.function = [function]
            print(self.function)
        else:
            self.function = function
        self.setGeometry(500, 100, 1500, 1500)
        self.setWindowTitle("Graph")

    def __get_zoom(self, zoom):
        if zoom < 0:
            return 50
        elif zoom == 0:
            return 50
        elif zoom == 1:
            return 25
        elif zoom == 2:
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

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        self.draw_graph(qp)
        for i in self.function:
            self.draw_function(qp, i)
        qp.end()

    def draw_graph(self, qp):
        self.draw_axes(qp)
        self.draw_grid(qp)

    def draw_axes(self, qp):
        # if the class instance zoom is not greater than 25, set it to 10
        # this makes sure the labels don't get too clumped together when the graph is very zoomed out
        if self.zoom >= 25:
            zoom = self.zoom
        else:
            zoom = 10

        horizontal_spacing: int
        vertical_spacing: int
        axes = QColor(0, 0, 0, 150)
        axes_pen = QPen(axes, 2, Qt.SolidLine)
        qp.setPen(axes_pen)
        qp.drawLine(0, 750, 1500, 750)
        qp.drawLine(750, 0, 750, 1500)

        font = QFont()
        font.setBold(True)
        font.setFixedPitch(True)
        font.setPointSize(self.__get_point_size())
        qp.setFont(font)
        # draws the last labels on the x-axis and y-axis
        #spacing = self.__get_spacing(-750)
        #qp.drawText(1, 780, str(int(-750 / self.zoom)))
        #qp.drawText(729 - spacing, 1485, str(int(-750 / self.zoom)))

        # draws the first labels on the x-axis and y-axis
        #spacing = self.__get_spacing(750)
        #qp.drawText(1470 - spacing, 780, str(int(750 / self.zoom)))
        #qp.drawText(729 - spacing, 10, str(int(750 / self.zoom)))

        # draws the zero label for both the x-axis and y-axis
        qp.drawText(730, 775, '0')

        # Draws the x-coordinate labels every major line
        for x in range(-750 + zoom * 5, 747, zoom * 5):
            x_label = int(x / self.zoom)
            horizontal_spacing = self.__get_horizontal_spacing(x_label)
            vertical_spacing = 10 - self.__get_point_size()
            x_label = str(x_label)
            if not x == 0:
                qp.drawText(x + 760 - horizontal_spacing, 780 - vertical_spacing , x_label)

        # Draws the y-coordinate labels every major line
        for y in range(-750 + zoom * 5, 750, zoom * 5):
            y_label = int(-y / self.zoom)
            horizontal_spacing = self.__get_horizontal_spacing(y_label)
            y_label = str(y_label)
            if y != 0:
                qp.drawText(745 - horizontal_spacing, y + 755, y_label)

    def __get_point_size(self):
        if self.zoom == 50:
            return 8
        elif self.zoom == 25:
            return 7
        elif self.zoom == 10:
            return 5
        elif self.zoom == 5:
            return 4
        elif self.zoom == 1:
            return 3

    def __get_horizontal_spacing(self, coordinate):
        spacing: int
        length = len(str(coordinate))
        spacing = self.__get_point_size()*2 * length
        return spacing

    def draw_grid(self, qp):
        major_grid = QColor(0, 0, 0, 50)
        minor_grid = QColor(0, 0, 0, 20)
        major_grid_pen = QPen(major_grid, 1, Qt.SolidLine)
        minor_grid_pen = QPen(minor_grid, 1, Qt.SolidLine)

        qp.setPen(major_grid_pen)
        # Draws a major horizontal lines every 5 minor lines
        for x in range(0, 1503, self.zoom * 5):
            qp.drawLine(x, 0, x, 1500)

        # Draws a major horizontal lines every 5 minor lines
        for y in range(0, 1503, self.zoom * 5):
            qp.drawLine(0, y, 1500, y)

        # Only draws the minor lines if the zoom level is below 2
        if self.minor_grid:
            qp.setPen(minor_grid_pen)
            # Draws minor horizontal lines in increments of the zoom instance variable
            for x in range(0, 1503, self.zoom):
                qp.drawLine(x, 0, x, 1500)

            # Draws minor horizontal lines in increments of the zoom instance variable
            for y in range(0, 1503, self.zoom):
                qp.drawLine(0, y, 1500, y)

    def draw_function(self, qp, function):
        y_float: float
        y: int
        continuous = True
        counter = -750
        calc = Calculator()
        pen = QPen(Qt.red, 6, Qt.SolidLine, Qt.RoundCap)
        pen.setJoinStyle(Qt.RoundJoin)
        pen.setCosmetic(True)
        qp.setPen(pen)
        qp.setRenderHint(QPainter.SmoothPixmapTransform, True)
        qp.setRenderHint(QPainter.Antialiasing, True)
        for x in range(-750, 1503):
            counter += 1
            try:
                x = float(x) / self.zoom
                print('x: ' + str(x))
                y_float = float(calc.PEMDAS(function.replace('x', ' ( ' + str(x) + ' ) ')))
                self.check_complex(y_float)
                # self.check_infinity(y_float)
                y = int(y_float * -1 * self.zoom + 750)
                point1 = [x * self.zoom + 750, y]
                # qp.drawPoint(*point1)
                break
            except ValueError:
                print('exception')
                pass

        for x in range(counter, 1503):
            try:
                x = float(x) / self.zoom
                print('x: ' + str(x))

                y_float = calc.PEMDAS(function.replace('x', ' ( ' + str(x) + ' ) '))
                self.check_complex(y_float)
                # self.check_infinity(y_float)
                y_float = float(y_float)
                print("y: " + str(y_float))
                y = int(y_float * -1 * self.zoom + 750)
                point2 = [x * self.zoom + 750, y]
                if not continuous:
                    point1 = point2
                    print(point1)
                    qp.drawPoint(*point1)
                elif continuous:
                    qp.drawLine(*point1, *point2)
                    point1 = point2
                continuous = True
            except:
                continuous = False

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
    logging.basicConfig(level=logging.DEBUG)
    app = QApplication(sys.argv)
    functions = ['√ x']
    widget = Graph(functions, 0)
    widget.show()
    sys.exit(app.exec_())
