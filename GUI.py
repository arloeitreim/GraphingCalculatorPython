from QtDesignerCode import Ui_MainWindow
import PyQt5
from PyQt5 import QtCore, QtGui, uic, QtWidgets
from PyQt5.QtWidgets import QWidget
from Calculator import Calculator

# converting .ui to .py: pyuic5: pyuic5 -x QtDesignerCode.ui -o QtDesignerCode.py
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

        self.count = "_"
        self.previous = ''

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
        self.multiplication.clicked.connect(lambda: self.add(" * "))
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
        #self.x.clicked.connect(lambda: self.add(' <span> 2 </span> '))
        self.answr.clicked.connect(lambda: self.add(self.previous))


    def clear_method(self):
        self.count = '_'
        self.equals.setText(self.count.replace('  ', ' '))
        self.equals.adjustSize()


    def arrows(self, direction):
        direction_int: int
        distance: int
        distance = 1
        underscore_index = self.count.index('_')
        self.count = self.count.replace('_', '')
        #if self.count[underscore_index - 5: underscore_index] == ('<sup>' or '<sub'):
            #self.count = self.count[:underscore_index - 5] + self.count[underscore_index]
        #elif self.count[underscore_index - 6: underscore_index] == ('</sup>' or '</sub'):
            #self.count = self.count[:underscore_index - 6] + self.count[underscore_index]
        if direction == 'left':
            direction_int = 1
            if self.count[underscore_index - 3: underscore_index] == 'log':
                print(self.count[underscore_index - 3: underscore_index])
                distance = 3
            elif (lambda x: (x == '<sup>') or (x == '<sub>'))(self.count[underscore_index - 5: underscore_index]):
            #if self.count[underscore_index - 5: underscore_index] == '<sup>' or self.count[underscore_index - 5: underscore_index] =='<sub>':
                distance = 5
            elif (lambda x: (x == '</sup>') or (x == '</sub>'))(self.count[underscore_index - 6: underscore_index]):
            #if self.count[underscore_index - 6: underscore_index] == ('</sup>' or '</sub>'):
                distance = 6
            #print(self.count[underscore_index - 1 * direction_int])
        elif direction == 'right':
            direction_int = -1
            #print(self.count[underscore_index:underscore_index + 5])

            if self.count[underscore_index: underscore_index + 3] == 'log':
                #print(self.count[underscore_index: underscore_index + 3])
                distance = 3
            elif (lambda x: (x == '<sup>') or (x == '<sub>'))(self.count[underscore_index: underscore_index + 5]):
            #if self.count[underscore_index: underscore_index + 5] == ('<sub>' or '<sup>'):
                distance = 5
            elif (lambda x: (x == '</sup>') or (x == '</sub>'))(self.count[underscore_index: underscore_index + 6]):
            #if self.count[underscore_index: underscore_index + 6] == ('</sup>' or '</sub>'):
                distance = 6
        self.count = self.count[:underscore_index - distance*direction_int] + '_' + self.count[underscore_index - distance*direction_int:]
        self.equals.setText(self.count.replace('  ', ' '))
        self.equals.adjustSize()



    def equals_method(self):
        self.translate_for_calculator()
        calc = Calculator()
        self.count = calc.PEMDAS(self.count) + '_'
        #self.count = self.count.replace("")
        self.previous = self.count
        self.equals.setText(self.count.replace('  ', ' '))
        self.equals.adjustSize()
        print(self.count)


    def translate_for_calculator(self):
        self.count = self.count.replace('_', '')
        self.count = self.count.replace('<sub>', '(')
        self.count = self.count.replace('<sup>', '^ (')
        self.count = self.count.replace('<span>', '(')
        self.count = self.count.replace('</sub>', ')')
        self.count = self.count.replace('</sup>', ')')
        self.count = self.count.replace('</span>', ')')

    def add_log(self):
        self.count = self.count.replace("_", ' log <sub> _ </sub>')
        self.equals.setText(self.count.replace('  ', ' '))
        self.equals.adjustSize()

    def add_exponent(self):
        self.count = self.count.replace("_", ' <sup> _ </sup>')
        self.equals.setText(self.count.replace('  ', ' '))
        self.equals.adjustSize()


    def add_sqrt(self):
        self.count = self.count.replace('_', ' √ <span> _ </span> ')
        self.equals.setText(self.count.replace('  ', ' '))
        self.equals.adjustSize()

    def delete(self):
        underscore_index = self.count.index('_')
        distance = self.find_distance(underscore_index)
        if not underscore_index - distance < 0:
            self.count = self.count[:underscore_index - distance] + self.count[underscore_index:]
        #replace = self.find_replace()
        #self.count = self.count.replace(replace, '')
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


    def find_distance(self, underscore_index):
        distance: int
        if self.count[underscore_index - 3: underscore_index] == 'log':
            distance = 3
        elif (lambda x: x == '<sup>' or x == '<sub>')(self.count[underscore_index - 5: underscore_index]):
            distance = 5
        elif (lambda x: x == '</sup>' or x == '</sub>' or x == '<span>')(self.count[underscore_index - 6: underscore_index]):
            distance = 6
        elif self.count[underscore_index - 7: underscore_index] == '</span>':
            distance = 7
        elif ' ' in self.count[underscore_index - 1]:
            distance = 2
        else:
            distance = 1
        return distance



    # text: text that will be added to count and displayed in the GUI
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
