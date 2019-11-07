"""Calculator."""

import re

class OperationIncomplete(ValueError):
    pass

class InvalidOperation(ValueError):
    pass

class NotAnInteger(ValueError):
    pass

class Calculator:
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
        """Evaluates server input and returns result."""

        # Remove multiple spaces
        message = message.strip()
        message = re.sub(' +', ' ', message)

        # Check for number of arguments
        params = message.split(' ')
        if len(params) < 3:
            raise OperationIncomplete('Not enough arguments')

        # Check for supported operations
        op = params[0]
        if op not in self.operations:
            raise InvalidOperation('Operation not supported')

        # TODO: ASK IF STRING CAN BE e.g. 2.0
        # Transform strings in integers
        try:
            a = int(params[1])
            b = int(params[2])
        except ValueError:
            raise NotAnInteger('One of the operands is not an integer')

        # Run operations and return result
        result = 0

        if op == '+':
            result = self.add(a, b)
        elif op == '-':
            result = self.subtract(a, b)
        elif op == '*':
            result = self.multiply(a, b)
        elif op == '/':
            result = self.divide(a, b)

        # Normalize float to int
        if type(result) is not int and result.is_integer():
            result = int(result)

        return result
