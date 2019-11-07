"""Client Agent."""
import socket
from http import HTTPRequest, HTTPParser

class Client:
    """TCP/UDP Client."""
    def __init__(self, buffer_size: int=1024):
        self.buffer_size = buffer_size
        self.client_socket = socket.socket(socket.AF_INET,
                                           socket.SOCK_STREAM)


class TCPClient(Client):
    """TCP Client."""

    def connect(self, host: str="127.0.0.1", port: int=50123):
        """Connect to server."""
        self.client_socket.connect((host, port))

    def send(self, message: str) -> bool:
        message_length = len(message)
        message = message.encode()

        total_sent = 0

        while total_sent < message_length:
            sent = self.client_socket.send(message[total_sent:])

            if sent == 0:
                raise RuntimeError("Connection broken")

            total_sent = total_sent + sent

    def http_send(self, message: str) -> bool:
        pass

    def receive(self, message: str) -> str:
        pass

    def request(self, message: str) -> str:
        return None

    def http_request(self, message: str) -> str:
        pass
