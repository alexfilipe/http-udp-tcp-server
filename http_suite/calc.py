"""Calculator module for performing basic arithmetic operations."""

import re


class OperationIncomplete(ValueError):
    """Exception raised when an operation is incomplete."""


class InvalidOperation(ValueError):
    """Exception raised for unsupported operations."""


class NotAnInteger(ValueError):
    """Exception raised when one or more operands are not integers."""


class Calculator:
    """A simple calculator for performing basic arithmetic operations."""

    def __init__(self):
        self.operations = set(["+", "-", "*", "/"])

    def add(self, a: int, b: int) -> int:
        """Add two integers.

        Args:
            a (int): The first integer.
            b (int): The second integer.

        Returns:
            int: The sum of the two integers.
        """
        return a + b

    def subtract(self, a: int, b: int) -> int:
        """Subtract the second integer from the first.

        Args:
            a (int): The first integer.
            b (int): The second integer.

        Returns:
            int: The result of the subtraction.
        """
        return a - b

    def multiply(self, a: int, b: int) -> int:
        """Multiply two integers.

        Args:
            a (int): The first integer.
            b (int): The second integer.

        Returns:
            int: The product of the two integers.
        """
        return a * b

    def divide(self, a: int, b: int) -> int:
        """Divide the first integer by the second.

        Args:
            a (int): The numerator.
            b (int): The denominator.

        Returns:
            int: The result of the division.

        Raises:
            ZeroDivisionError: If the denominator is zero.
        """
        if b == 0:
            raise ZeroDivisionError("Division by zero not allowed")

        return a / b

    def evaluate(self, message: str) -> str:
        """Evaluate a string message containing an arithmetic operation.

        Args:
            message (str): The input string containing the operation and operands.

        Returns:
            str: The result of the operation as a string.

        Raises:
            OperationIncomplete: If the input does not contain enough arguments.
            InvalidOperation: If the operation is not supported.
            NotAnInteger: If one or more operands are not integers.
        """
        # Remove multiple spaces
        message = message.strip()
        message = re.sub(" +", " ", message)

        # Check for number of arguments
        params = message.split(" ")
        if len(params) < 3:
            raise OperationIncomplete("Not enough arguments")

        # Check for supported operations
        op = params[0]
        if op not in self.operations:
            raise InvalidOperation("Operation not supported")

        # Transform strings into integers
        try:
            a = int(params[1])
            b = int(params[2])
        except ValueError:
            raise NotAnInteger("One of the operands is not an integer")

        # Run operations and return result
        result = 0

        if op == "+":
            result = self.add(a, b)
        elif op == "-":
            result = self.subtract(a, b)
        elif op == "*":
            result = self.multiply(a, b)
        elif op == "/":
            result = self.divide(a, b)

        # Normalize float to int
        if type(result) is not int and result.is_integer():
            result = int(result)

        return str(result)
