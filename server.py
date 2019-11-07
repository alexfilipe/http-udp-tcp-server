"""TCP/UDP Servers."""

from calc import Calculator, OperationIncomplete, InvalidOperation
import socket

class Server:
    """UDP/TCP server with Sockets."""

    def __init__(self, host: str="127.0.0.1", port: int=50123,
                 buffer_size: int=1024):

        self.host = host
        self.port = port
        self.buffer_size = buffer_size

        self.server_socket = socket.socket(socket.AF_INET,
                                           socket.SOCK_STREAM)
        self.server_socket.bind((host, port))
        self.server_socket.listen(1)

    def run(self):
        raise NotImplementedError


class TCPServer(Server):
    """Reliable TCP Server."""

    def run(self):
        print("Starting TCP Server...")

        client_socket, address = self.server_socket.accept()

        while True:
            data = client_socket.recv(self.buffer_size)

            if not data:
                break

            print("received data:", data)
            client_socket.send("data received")

        client_socket.close()


class UDPReliableServer(Server):
    """UDP Server running on reliable environment."""
    pass


class UDPUnreliableServer(Server):
    """UDP Server running on unreliable environment."""
    pass
