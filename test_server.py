from server import (HTTPRequest, HTTPResponse,
                    Calculator, InvalidOperation,
                    OperationIncomplete)


http_req = HTTPRequest(host="localhost")

print(http_req.build_request(
    method="POST",
    params={
        "expression": "+ 1 2"
    }
))

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
