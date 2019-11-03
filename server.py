import re

class OperationIncomplete(ValueError):
    pass

class InvalidOperation(ValueError):
    pass

class Server:
    def __init__(self):
        self.operations = set(['+', '-', '*', '/'])

    def add(self, a: int, b: int) -> int:
        return a + b

    def subtract(self, a: int, b: int) -> int:
        return a - b

    def multiply(self, a: int, b: int) -> int:
        return a * b

    def divide(self, a: int, b: int) -> int:
        if b == 0:
            raise ZeroDivisionError('Division by zero not allowed')

        return a / b

    def evaluate(self, message: str) -> str:
        message = re.sub(' +', ' ', message)

        params = message.split(' ')

        if len(params) > 3:
            raise OperationIncomplete('Not enough arguments')

        op = params[0]

        if op not in self.operations:
            raise InvalidOperation('Operation not supported')

        result = 0

        a = int(params[1])
        b = int(params[2])

        if op == '+':
            result = self.add(a, b)
        elif op == '-':
            result = self.subtract(a, b)
        elif op == '*':
            result = self.multiply(a, b)
        elif op == '/':
            result = self.divide(a, b)

        return result


if __name__ == "__main__":
    server = Server()
    print('Result:', server.evaluate("+  1   3"))
    print('Result:', server.evaluate("/ 1   3"))
    print('Result:', server.evaluate("/ 1 0"))
