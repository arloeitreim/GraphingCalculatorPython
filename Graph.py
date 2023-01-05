from Calculator import Calculator
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtCore import Qt
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QFont
import sys
import PyQt5
from math import isinf

if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    PyQt5.QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    PyQt5.QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)


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
        self.setGeometry(500, 100, 500, 500)
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
        for i in range(len(self.function)):
            self.draw_function(qp, self.function[i])
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

        spacing: int
        axes = QColor(0, 0, 0, 150)
        axes_pen = QPen(axes, 2, Qt.SolidLine)
        qp.setPen(axes_pen)
        qp.drawLine(0, 250, 500, 250)
        qp.drawLine(250, 0, 250, 500)

        font = QFont()
        font.setBold(True)
        font.setFixedPitch(True)
        font.setPointSize(7)
        qp.setFont(font)
        # draws the last labels on the x-axis and y-axis
        spacing = self.__get_spacing(-250)
        qp.drawText(1, 260, str(int(-250 / self.zoom)))
        qp.drawText(243 - spacing, 495, str(int(-250 / self.zoom)))

        # draws the first labels on the x-axis and y-axis
        spacing = self.__get_spacing(250)
        qp.drawText(490 - spacing, 260, str(int(250 / self.zoom)))
        qp.drawText(243 - spacing, 10, str(int(250 / self.zoom)))

        # draws the zero label for both the x-axis and y-axis
        qp.drawText(239, 260, '0')

        # Draws the x-coordinate labels every major line
        for x in range(-250 + zoom * 5, 249, zoom * 5):
            spacing = self.__get_spacing(x)
            x_label = str(int(x / self.zoom))
            if not x == 0:
                qp.drawText(x + 249 - spacing, 260, x_label)

        # Draws the y-coordinate labels every major line
        for y in range(-250 + zoom * 5, 250, zoom * 5):
            spacing = self.__get_spacing(-y)
            y_label = str(int(-y / self.zoom))
            if y != 0:
                qp.drawText(243 - spacing, y + 255, y_label)

    def __get_spacing(self, coordinate):
        if self.zoom >= 25:
            zoom = self.zoom
        else:
            zoom = 10
        spacing: int
        coordinate = str(int(coordinate / zoom))
        length = len(coordinate)
        spacing = 5 * length
        return spacing

    def draw_grid(self, qp):
        major_grid = QColor(0, 0, 0, 50)
        minor_grid = QColor(0, 0, 0, 20)
        major_grid_pen = QPen(major_grid, 1, Qt.SolidLine)
        minor_grid_pen = QPen(minor_grid, 1, Qt.SolidLine)

        qp.setPen(major_grid_pen)
        # Draws a major horizontal lines every 5 minor lines
        for x in range(0, 501, self.zoom * 5):
            qp.drawLine(x, 0, x, 500)

        # Draws a major horizontal lines every 5 minor lines
        for y in range(0, 501, self.zoom * 5):
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

    def draw_function(self, qp, function):
        y_float: float
        y: int
        continuous = True
        counter = -250
        calc = Calculator()
        pen = QPen(Qt.red, 3, Qt.SolidLine, Qt.RoundCap)
        qp.setPen(pen)
        for x in range(-250, 251):
            counter += 1
            try:
                x = float(x) / self.zoom
                print('x: ' + str(x))
                y_float = float(calc.PEMDAS(function.replace('x', ' ( ' + str(x) + ' ) ')))
                self.check_complex(y_float)
                # self.check_infinity(y_float)
                y = int(y_float * -1 * self.zoom + 250)
                point1 = [x * self.zoom + 250, y]
                # qp.drawPoint(*point1)
                break
            except ValueError:
                print('exception')
                pass

        for x in range(counter, 251):
            try:
                x = float(x) / self.zoom
                print('x: ' + str(x))
                y_float = calc.PEMDAS(function.replace('x', ' ( ' + str(x) + ' ) '))
                self.check_complex(y_float)
                # self.check_infinity(y_float)
                y_float = float(y_float)
                print("y: " + str(y_float))
                y = int(y_float * -1 * self.zoom + 250)
                point2 = [x * self.zoom + 250, y]
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
    app = QApplication(sys.argv)
    functions = ['√ x']
    widget = Graph(functions, 1)
    widget.show()
    sys.exit(app.exec_())
