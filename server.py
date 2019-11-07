"""TCP/UDP Calculator Servers."""

from calc import Calculator, OperationIncomplete, InvalidOperation
from http import HTTPResponse, HTTPParser
import socket

class Server:
    """UDP/TCP server with Sockets."""

    def __init__(self, host: str="127.0.0.1", port: int=51234,
                 buffer_size: int=1024):

        self.host = host
        self.port = port
        self.buffer_size = buffer_size

        self.server_socket = socket.socket(socket.AF_INET,
                                           socket.SOCK_STREAM)
        self.server_socket.bind((host, port))
        self.server_socket.listen(1)

    def process(self, message: str) -> str:
        """Processes HTTP request and returns response."""
        parser = HTTPParser()
        response = HTTPResponse()

        request = parser.parse_request(message)
        # print("processed request:\n", request)

        # Invalid request (no expression sent)
        if (not request["params"]
            or "expression" not in request["params"]):
            return response.build_response(status=406, data="-1")

        expression = request["params"]["expression"][0]
        print("expression received:", expression)

        return "nope"


    def run(self):
        raise NotImplementedError


class TCPServer(Server):
    """Reliable TCP Server."""

    def run(self):
        """Runs server until Control+C is called."""

        print("TCP server started.")

        client_socket, address = self.server_socket.accept()

        while True:
            data = client_socket.recv(self.buffer_size)

            if data:
                print("Received data:\n", data.decode())

                response = self.process(data.decode())
                client_socket.send(response.encode())
            else:
                print("Connection ended.")
                break

        client_socket.close()


class UDPReliableServer(Server):
    """UDP Server running on reliable environment."""
    pass


class UDPUnreliableServer(Server):
    """UDP Server running on unreliable environment."""
    pass
