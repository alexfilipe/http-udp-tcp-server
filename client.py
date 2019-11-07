"""Client Agent."""
import socket
from http import HTTPRequest, HTTPParser

class Client:
    """TCP/UDP Client."""
    def __init__(self, buffer_size: int=1024):
        self.buffer_size = buffer_size
        self.client_socket = socket.socket(socket.AF_INET,
                                           socket.SOCK_STREAM)

    def send(self, message: str):
        raise NotImplementedError

    def receive(self) -> str:
        raise NotImplementedError

    def http_send(self, host: str="127.0.0.1", file: str="/",
                  method: str="GET", params: dict=None, data: str=None):

        http_req = HTTPRequest(host=host)
        request = http_req.build_request(
            file=file,
            method=method,
            params=params,
            data=data
        )

        self.send(request)



class TCPClient(Client):
    """TCP Client."""

    def connect(self, host: str="127.0.0.1", port: int=51234):
        """Connect to server."""
        self.client_socket.connect((host, port))

    def send(self, message: str):
        message_length = len(message)
        message = message.encode()

        total_sent = 0

        while total_sent < message_length:
            sent = self.client_socket.send(message[total_sent:])

            if sent == 0:
                raise RuntimeError("Connection broken")

            total_sent = total_sent + sent

    def receive(self) -> str:
        chunk = self.client_socket.recv(self.buffer_size)

        if chunk == b"":
            raise RuntimeError("Connection broken")

        return chunk
