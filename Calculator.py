import math
from math import sqrt

class Calculator:

    def __init__(self, count = -1):
        self.count = count
        if count != -1:
            self.count = self.PEMDAS(self.count)

    def PEMDAS(self, count):
        count = count.replace('  ', ' ')
        # Order of Operations
        # returns result of count
        try:
            while '(' in count and ')' in count:
                count = self.parentheses(count)
                count = count.replace('  ', ' ')
            while '^' in count or '√' in count or 'log' in count:
                count = self.exponents_sqrts_and_log(count)
            while '*' in count or '/' in count:
                count = self.multiplication_and_division(count)
            while '+' in count or '-' in count:
                count = self.addition_and_subtraction(count)
            if float(count).is_integer():
                count = str(int(float(count)))
            return count
        except ValueError:
            return "Error"

    def parentheses(self, count: str):
        # P in PEMDAS
        # Parses operations inside of parentheses

        # indice of count before the closest close parenthisis
        before_close_parenth = count[:count.index(')')]

        # last open parenthisis before the first close parenthisis
        last_open_parenth = before_close_parenth.rfind('(')

        # indice of count between the last open parenthesis and first close parenthesis
        # includes parentheses
        subCount = count[last_open_parenth : count.index(')') + 1]

        # excludes parentheses from subCount
        # finds results using PEMDAS method
        replacement = self.PEMDAS(subCount[2:len(subCount) - 2])

        count = count.replace(subCount, replacement)
        return count


    def exponents_sqrts_and_log(self, count):
        # E in PEMDAS
        # Parses exponents and square roots into float
        components = count.split(' ')
        un_operated: float
        operated: float
        for i in range(len(components)):
            if '^' in components[i]:
                un_operated = components[i - 1] + ' ^ ' + components[i + 1]
                operated = str(float(components[i - 1]) ** float(components[i + 1]))
                # replaces unoperated version with operated version in count
                count = count.replace(un_operated, operated)
            elif "√" in components[i]:
                un_operated = '√ ' + components[i + 1]
                operated = str( sqrt(float(components[i + 1])))
                # replaces unoperated version with operated version in count
                count = count.replace(un_operated, operated)
            elif 'log' in components[i]:
                un_operated = 'log ' + components[i + 1] + ' ' + components[i + 2]
                operated = str( math.log(float(components[i + 2]), float(components[i + 1])))
                count = count.replace(un_operated, operated)
        return count


    def multiplication_and_division(self, count):
        # M and D in PEMDAS
        # Parses multiplication and division operations into float
        components = count.split(' ')
        un_operated: float
        operated: float
        for i in range(len(components)):
            if '*' in components[i]:
                un_operated = components[i - 1] + ' * ' + components[i + 1]
                operated = str(float(components[i - 1]) * float(components[i + 1]))
                count = count.replace(un_operated, operated)
            elif "/" in components[i]:
                un_operated = components[i - 1] + ' / ' + components[i + 1]
                operated = str(float(components[i - 1]) / float(components[i + 1]))
                count = count.replace(un_operated, operated)
        return count


    def addition_and_subtraction(self, count):
        # A and S in PEMDAS
        # Parses addition and subtraction operations into float
        components = count.split(' ')
        un_operated: float
        operated: float
        for i in range(len(components)):
            if '+' in components[i]:
                un_operated = components[i - 1] + ' + ' + components[i + 1]
                operated = str(float(components[i - 1]) + float(components[i + 1]))
                count = count.replace(un_operated, operated)
            elif "-" in components[i]:
                un_operated = components[i - 1] + ' - ' + components[i + 1]
                operated = str(float(components[i - 1]) - float(components[i + 1]))
                count = count.replace(un_operated, operated)
        return count

    def getCount(self):
        # Returns count instance
        return self.count


if __name__ == "__main__":
    calc = Calculator()
    # res = calc.parentheses('4 + ( 2 + 3 ) + 4')
    #res = calc.exponents_and_sqrts('√ 4')
    res = calc.PEMDAS('log 2 3')
    print(f'<{res}>')
    print('√')
    print('÷')
