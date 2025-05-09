from http_suite.calc import (
    Calculator,
    InvalidOperation,
    NotAnInteger,
    OperationIncomplete,
)

calc = Calculator()

print(calc.evaluate("+ 1 2"))
print(calc.evaluate("/ 12 3"))

try:
    print(calc.evaluate("/ 2 0"))
except ZeroDivisionError as e:
    print(str(e))

print(calc.evaluate("+ 2 3 4"))

try:
    print(calc.evaluate("* 2"))
except OperationIncomplete as e:
    print(str(e))

try:
    print(calc.evaluate("& 2 3"))
except InvalidOperation as e:
    print(str(e))


try:
    print(calc.evaluate("/ 2 3.4"))
except NotAnInteger as e:
    print(str(e))
