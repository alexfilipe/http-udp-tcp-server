import re
import socket
from email.utils import formatdate

class OperationIncomplete(ValueError):
    pass

class InvalidOperation(ValueError):
    pass

class Status406(SystemError):
    pass

class HTTPRequest:
    pass

class HTTPResponse:
    def __init__(self):
        self.http_version = "HTTP/1.1"

        self.status_codes = {
            200: "200 OK",
            406: "406 Not Acceptable"
        }

        self.content_type = "text/plain"

        self.server = "calculator/0.1"

        self.response_template = (
            "{version} {{status}}\n"
            "Date: {{date}}\n"
            "Content-Type: {content_type}\n"
            "Server: {server}\n"
            "\n{{data}}"
        )

        self.response_template = self.response_template.format(
            version=self.http_version,
            server=self.server,
            content_type=self.content_type
        )

    def gmt_date(self):
        """Return current datetime in GMT format."""
        return formatdate(timeval=None, localtime=False, usegmt=True)

    def build_200(self, data: str) -> str:
        """Build 200 OK response."""
        if data is None:
            data = ""

        response = self.response_template.format(
            status=self.status_codes[200],
            date=self.gmt_date(),
            data=data
        )

        return response

    def build_response(self, data: str, status: int=200) -> str:
        """Build the HTTP response."""
        response = ""

        if status == 200:
            response = self.build_200(data)
        elif status == 300:
            pass

        return response


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
        message = re.sub(' +', ' ', message)

        # Check for number of arguments
        params = message.split(' ')
        if len(params) < 3:
            raise OperationIncomplete('Not enough arguments')

        # Check for supported operations
        op = params[0]
        if op not in self.operations:
            raise InvalidOperation('Operation not supported')

        # Run operations and return result
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


class Server:
    """UDP server with Sockets."""

    def __init__(self, host: str='127.0.0.1', port: int=50001):
        self.host = host
        self.port = port

    def run_server(self):
        pass


class UDPServer(Server):
    pass


class TCPServer(Server):
    pass


if __name__ == "__main__":
    response = HTTPResponse()

    print(response.build_response(status=200, data='hello'))

    calc = Calculator()
    print('Result:', calc.evaluate("+  1   3"))
    print('Result:', calc.evaluate("/ 1   3"))
    # print('Result:', calc.evaluate("/ 1 0"))
