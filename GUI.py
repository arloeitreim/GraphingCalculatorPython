import math
from QtDesignerCode import Ui_MainWindow
import PyQt5
from PyQt5 import QtCore, QtGui, uic, QtWidgets
from PyQt5.QtWidgets import QWidget
from Calculator import Calculator
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtCore import Qt
import sys
from GraphGUI import GraphGUI
from RegressionGUI import RegressionGUI

# converting .ui to .py:
# opening designer: pyqt5-tools designer

# Scales GUI to resolution
# without this the GUI appears very small on high resolution screens

if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    PyQt5.QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    PyQt5.QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

# SuperClass is Ui_MainWindow
# Everything inherited from Ui_MainWindow was made in QtDesigner
# Everything else was manually coded
class GUI(Ui_MainWindow):
    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        MainWindow.setWindowTitle('Calculator')

        self.count = "_"
        self.previous = ''
        self.functions: list[str] = []
        self.remove_function_actions = dict()
        self.graph = GraphGUI([])
        self.regression = RegressionGUI()

        MainWindow.move(300, 100)

        # buttons execute connected method when pressed

        self.zero.clicked.connect(lambda: self.add("0"))
        self.one.clicked.connect(lambda: self.add("1"))
        self.two.clicked.connect(lambda: self.add("2"))
        self.three.clicked.connect(lambda: self.add("3"))
        self.four.clicked.connect(lambda: self.add("4"))
        self.five.clicked.connect(lambda: self.add("5"))
        self.six.clicked.connect(lambda: self.add("6"))
        self.seven.clicked.connect(lambda: self.add("7"))
        self.eight.clicked.connect(lambda: self.add("8"))
        self.nine.clicked.connect(lambda: self.add("9"))
        self.point.clicked.connect(lambda: self.add("."))
        self.del_button.clicked.connect(lambda: self.delete())
        self.addition.clicked.connect(lambda: self.add(" + "))
        self.subtraction.clicked.connect(lambda: self.add(" - "))
        self.multiplication.clicked.connect(lambda: self.add(" × "))
        self.division.clicked.connect(lambda: self.add(" ÷ "))
        self.power.clicked.connect(lambda: self.add_exponent())
        self.root.clicked.connect(lambda: self.add_sqrt())
        self.log.clicked.connect(lambda: self.add_log())
        self.negative.clicked.connect(lambda: self.add("-"))
        self.left_parenth.clicked.connect(lambda: self.add(" ( "))
        self.right_parenth.clicked.connect(lambda: self.add(" ) "))
        self.left_arrow.clicked.connect(lambda: self.arrows('left'))
        self.right_arrow.clicked.connect(lambda: self.arrows('right'))
        self.clear.clicked.connect(lambda: self.clear_method())
        self.equals_button.clicked.connect(lambda: self.equals_method())
        self.x.clicked.connect(lambda: self.add('x'))
        self.answr.clicked.connect(lambda: self.add(self.previous))
        self.pi.clicked.connect(lambda: self.add("π"))
        self.z.clicked.connect(lambda: self.add('z'))
        
        self.actionView_2.triggered.connect(lambda: self.view())
        self.actionAdd_Function.triggered.connect(lambda: self.addFunction())

        self.menu_remove_function = QtWidgets.QMenu(self.menuGraph)
        self.menuGraph.addAction(self.menu_remove_function.menuAction())

        self.action_regression = QtWidgets.QAction(MainWindow)
        self.menubar.addAction(self.action_regression)
        self.action_regression.triggered.connect(lambda: self.regression.show())
        self.name_actions()


    def name_actions(self):
        _translate = QtCore.QCoreApplication.translate
        self.menu_remove_function.setTitle(_translate("MainWindow", 'Remove Function'))
        self.action_regression.setText('Regression')

    def addFunction(self):
        if len(self.functions) == 4:
            exit()
        without_html = Calculator.translate(self.count)
        with_html = self.count.replace('_', '')
        self.functions.append(with_html)

        self.remove_function_actions[without_html] = QtWidgets.QAction(self.menu_remove_function)
        self.remove_function_actions[without_html].triggered.connect(lambda: self.remove_function(without_html))

        self.menu_remove_function.addAction(self.remove_function_actions[without_html])

        _translate = QtCore.QCoreApplication.translate
        self.remove_function_actions[without_html].setText(_translate("MainWindow", without_html))

    def remove_function(self, function):
        position_of_function = self.functions.index(function)

        del self.remove_function_actions[function]
        del self.functions[position_of_function]


    def view(self):
        self.graph = GraphGUI(self.functions)
        self.graph.show()


    def clear_method(self):
        self.count = '_'
        self.equals.setText(self.count.replace('  ', ' '))
        self.equals.adjustSize()


    def arrows(self, direction):
        distance:int
        direction_int: int
        underscore_index = self.count.index('_')
        self.count = self.count.replace('_', '')
        distance = self.find_distance(underscore_index, direction)

        if direction == 'left':
            direction_int = 1

        else:
            direction_int = -1

        self.count = self.count[:underscore_index - distance*direction_int] + '_' + self.count[underscore_index - distance*direction_int:]
        self.equals.setText(self.count.replace('  ', ' '))
        self.equals.adjustSize()



    def equals_method(self):
        calc = Calculator()

        self.count = calc.PEMDAS(self.count) + '_'
        self.previous = self.count

        self.equals.setText(self.count.replace('  ', ' '))
        self.equals.adjustSize()


    def add_log(self):
        self.count = self.count.replace("_", 'log<sub>_</sub>')

        self.equals.setText(self.count.replace('  ', ' '))
        self.equals.adjustSize()

    def add_exponent(self):
        self.count = self.count.replace("_", ' <sup>_</sup>')

        self.equals.setText(self.count.replace('  ', ' '))
        self.equals.adjustSize()


    def add_sqrt(self):
        self.count = self.count.replace('_', '√<span>_</span> ')

        self.equals.setText(self.count.replace('  ', ' '))
        self.equals.adjustSize()


    def delete(self):
        underscore_index = self.count.index('_')
        distance = self.find_distance(underscore_index)

        if not underscore_index - distance < 0:
            self.count = self.count[:underscore_index - distance] + self.count[underscore_index:]

        replace = self.find_replace()
        self.count = self.count.replace(replace, '')

        self.equals.setText(self.count.replace('  ', ' '))
        self.equals.adjustSize()


    def find_replace(self):
        replace = ''

        if (not '<sup>' in self.count) and ('</sup>' in self.count):
            replace = '</sup>'

        elif (not '<sub>' in self.count) and ('</sub>' in self.count):
            replace = '</sub>'

        elif ( not '<span>' in self.count) and ('</span>' in self.count):
            replace = '</span>'

        return replace


    def find_distance(self, underscore_index, direction='left', was_space=False):
        if direction == 'left':
            if was_space:
                underscore_index = underscore_index - 1

            distance_1 = self.count[underscore_index - 1]
            distance_3 = self.count[underscore_index - 3: underscore_index]
            distance_5 = self.count[underscore_index - 5: underscore_index]
            distance_6 = self.count[underscore_index - 6: underscore_index]
            distance_7 = self.count[underscore_index - 7: underscore_index]

        elif direction == 'right':
            if underscore_index + 1 == len(self.count):
                return 1

            if underscore_index + 1 > len(self.count):
                return 0

            if was_space:
                underscore_index = underscore_index + 1

            distance_1 = self.count[underscore_index + 1]
            distance_3 = self.count[underscore_index: underscore_index + 3]
            distance_5 = self.count[underscore_index: underscore_index + 5]
            distance_6 = self.count[underscore_index: underscore_index + 6]
            distance_7 = self.count[underscore_index: underscore_index + 7]

        if distance_3 == 'log':
            distance = 3

        elif (lambda x: x == '<sup>' or x == '<sub>')(distance_5):
            distance = 5

        elif (lambda x: x == '</sup>' or x == '</sub>' or x == '<span>')(distance_6):
            distance = 6

        elif distance_7 == '</span>':
            distance = 7

        elif distance_1 == ' ':
            # if distance_1 is a space, run find_distance() again, but with was_space set to true
            distance = self.find_distance(underscore_index, direction, True) + 1

        else:
            distance = 1

        return distance


    def add(self, text):
        self.count = self.count.replace("_", text + "_")
        self.equals.setText(self.count.replace('  ', ' '))
        self.equals.adjustSize()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = GUI()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
