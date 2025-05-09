"""Client Agent."""

import re
import socket

from .bcolors import bcolors
from .http import HTTPParser, HTTPRequest


class TimeoutException(SystemError):
    """Exception raised when a timeout occurs."""

    pass


def parse_expression(expression: str) -> dict:
    """Evaluates the expression and returns a dict with the operands and operator.

    Args:
        expression (str): The expression to parse.

    Returns:
        dict: A dictionary containing the operator and operands.
    """
    expression = expression.strip()
    expression = re.sub(" +", " ", expression)
    params = expression.split(" ")

    op = None
    a = None
    b = None

    if len(params) > 0:
        op = params[0]
    if len(params) > 1:
        a = params[1]
    if len(params) > 2:
        b = params[2]

    return {"op": op, "a": a, "b": b}


class Client:
    """Base class for TCP/UDP clients.

    Args:
        buffer_size (int): Size of the buffer for receiving data.
        debug (bool): Enable or disable debug mode.
    """

    def __init__(
        self,
        buffer_size: int = 1024,
        debug: bool = False,
    ):
        self.debug = debug
        self.buffer_size = buffer_size

    def send(self, message: str):
        """Send a message to the server.

        Args:
            message (str): The message to send.
        """
        raise NotImplementedError

    def receive(self) -> str:
        """Receive a message from the server.

        Returns:
            str: The received message.
        """
        raise NotImplementedError

    def process_response(self, message: str) -> str:
        """Process the server's response.

        Args:
            message (str): The response message.

        Returns:
            str: The processed response.
        """
        parser = HTTPParser()
        response = parser.parse_response(message)

        if response["status"] == 200:
            return response["data"]
        else:
            return False

    def result(self) -> str:
        """Get the result from the server.

        Returns:
            str: The processed response.
        """
        response = self.receive().decode()
        return self.process_response(response)


class TCPClient(Client):
    """TCP Client for communicating with a server.

    Args:
        buffer_size (int): Size of the buffer for receiving data.
        debug (bool): Enable or disable debug mode.
    """

    def __init__(
        self,
        buffer_size: int = 1024,
        debug: bool = False,
    ):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        super().__init__(buffer_size, debug)

    def connect(self, host: str = "127.0.0.1", port: int = 51234):
        """Connect to the server.

        Args:
            host (str): The server's hostname or IP address.
            port (int): The server's port number.
        """
        if self.debug:
            print(
                "{}{}Connecting to {}...{}".format(
                    bcolors.BOLD, bcolors.OKBLUE, host, bcolors.ENDC
                )
            )

        try:
            self.client_socket.connect((host, port))
        except ConnectionRefusedError:
            print(
                "{}{}Error: Connection refused.{}".format(
                    bcolors.BOLD, bcolors.FAIL, bcolors.ENDC
                )
            )

    def send(self, message: str):
        """Send a message to the server.

        Args:
            message (str): The message to send.
        """
        message_length = len(message)
        message = message.encode()

        total_sent = 0

        while total_sent < message_length:
            sent = self.client_socket.send(message[total_sent:])

            if sent == 0:
                raise RuntimeError("Connection broken")

            total_sent = total_sent + sent

    def http_send(
        self,
        host: str = "127.0.0.1",
        file: str = "/",
        method: str = "GET",
        params: dict = None,
        data: str = None,
    ):
        """Send an HTTP request to the server.

        Args:
            host (str): The server's hostname or IP address.
            file (str): The file path in the HTTP request.
            method (str): The HTTP method (e.g., GET, POST).
            params (dict): Query parameters for the request.
            data (str): Data to include in the request body.
        """
        http_req = HTTPRequest(host=host)
        request = http_req.build_request(
            file=file, method=method, params=params, data=data
        )

        if self.debug:
            print(
                "{}{}Sending HTTP Request...{}".format(
                    bcolors.BOLD, bcolors.OKBLUE, bcolors.ENDC
                )
            )
            print(request)

        self.send(request)

    def receive(self) -> str:
        """Receive a response from the server.

        Returns:
            str: The received response.
        """
        chunk = self.client_socket.recv(self.buffer_size)

        if chunk == b"":
            raise RuntimeError("Connection broken")

        if self.debug:
            print(
                "\n{}{}Received response:{}\n{}".format(
                    bcolors.BOLD, bcolors.OKBLUE, bcolors.ENDC, chunk.decode()
                )
            )

        return chunk


class UDPReliableClient(Client):
    """Reliable UDP Client for communicating with a server.

    Args:
        buffer_size (int): Size of the buffer for receiving data.
        server_port (int): The port number to bind the client socket.
        server_addr (str): The address to bind the client socket.
        debug (bool): Enable or disable debug mode.
    """

    def __init__(
        self,
        buffer_size: int = 1024,
        server_port: int = 50321,
        server_addr: int = "127.0.0.1",
        debug: bool = False,
    ):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.server_port = server_port
        self.server_addr = server_addr

        self.server_socket.bind((server_addr, server_port))

        self.MAX_TIMEOUT = 2.0

        super().__init__(buffer_size, debug)

    def send(self, message: str = None, host: str = "127.0.0.1", port: int = 50123):
        """Send a message to the server.

        Args:
            message (str): The message to send.
            host (str): The server's hostname or IP address.
            port (int): The server's port number.
        """
        if message is None:
            message = ""
        message = message.encode()

        self.server_socket.sendto(message, (host, port))

    def http_send(
        self,
        host: str = "127.0.0.1",
        port: int = 50123,
        file: str = "/",
        method: str = "GET",
        params: dict = None,
        data: str = None,
    ):
        """Send an HTTP request to the server.

        Args:
            host (str): The server's hostname or IP address.
            port (int): The server's port number.
            file (str): The file path in the HTTP request.
            method (str): The HTTP method (e.g., GET, POST).
            params (dict): Query parameters for the request.
            data (str): Data to include in the request body.
        """
        http_req = HTTPRequest(host=host)
        request = http_req.build_request(
            file=file, method=method, params=params, data=data
        )

        if self.debug:
            print(
                "{}{}Sending HTTP Request...{}".format(
                    bcolors.BOLD, bcolors.OKBLUE, bcolors.ENDC
                )
            )
            print(request)

        self.send(message=request, host=host, port=port)

    def receive(self) -> str:
        """Receive a response from the server.

        Returns:
            str: The received response.
        """
        data, addr = self.server_socket.recvfrom(self.buffer_size)

        if data == b"":
            raise RuntimeError("Connection broken")

        else:
            print(
                "\n{}{}Received response:{}\n{}".format(
                    bcolors.BOLD, bcolors.OKBLUE, bcolors.ENDC, data.decode()
                )
            )

        return data


class UDPUnreliableClient(Client):
    """Unreliable UDP Client for communicating with a server.

    Args:
        buffer_size (int): Size of the buffer for receiving data.
        server_port (int): The port number to bind the client socket.
        server_addr (str): The address to bind the client socket.
        debug (bool): Enable or disable debug mode.
        max_timeout (float): Maximum timeout for retries.
    """

    def __init__(
        self,
        buffer_size: int = 1024,
        server_port: int = 50321,
        server_addr: int = "127.0.0.1",
        debug: bool = False,
        max_timeout: float = 2.0,
    ):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.server_port = server_port
        self.server_addr = server_addr

        self.server_socket.bind((server_addr, server_port))

        self.max_timeout = max_timeout

        super().__init__(buffer_size, debug)

    def send(
        self,
        message: str = None,
        host: str = "127.0.0.1",
        port: int = 50123,
    ):
        """Send a message to the server.

        Args:
            message (str): The message to send.
            host (str): The server's hostname or IP address.
            port (int): The server's port number.
        """
        if message is None:
            message = ""
        message = message.encode()

        self.server_socket.sendto(message, (host, port))

    def http_req(
        self,
        host: str = "127.0.0.1",
        port: int = 50123,
        file: str = "/",
        method: str = "GET",
        params: dict = None,
        data: str = None,
    ):
        """Send an HTTP request to the server with retries.

        Args:
            host (str): The server's hostname or IP address.
            port (int): The server's port number.
            file (str): The file path in the HTTP request.
            method (str): The HTTP method (e.g., GET, POST).
            params (dict): Query parameters for the request.
            data (str): Data to include in the request body.

        Returns:
            str: The processed response.

        Raises:
            TimeoutException: If the maximum timeout is exceeded.
        """
        http_req = HTTPRequest(host=host)
        request = http_req.build_request(
            file=file, method=method, params=params, data=data
        )

        current_timeout = 0.1

        while True:
            self.server_socket.settimeout(current_timeout)

            if self.debug:
                print(
                    "{}{}Sending HTTP Request...{}".format(
                        bcolors.BOLD, bcolors.OKBLUE, bcolors.ENDC
                    )
                )
                print(request)

            self.send(message=request, host=host, port=port)

            if current_timeout > self.max_timeout:
                raise TimeoutException("Timeout exceeded.")

            try:
                data, addr = self.server_socket.recvfrom(self.buffer_size)

                if data == b"":
                    raise RuntimeError("Connection broken")
                else:
                    print(
                        "\n{}{}Received response:{}\n{}".format(
                            bcolors.BOLD, bcolors.OKBLUE, bcolors.ENDC, data.decode()
                        )
                    )
                    return self.process_response(data.decode())

            except socket.timeout:
                print("Request timed out. Trying again...\n")
                current_timeout *= 2
                continue
