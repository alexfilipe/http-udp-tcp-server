"""TCP/UDP Server."""

from calc import Calculator, OperationIncomplete, InvalidOperation
import socket

class Server:
    """UDP/TCP server with Sockets."""

    def __init__(self, host: str='127.0.0.1', port: int=50001):
        self.host = host
        self.port = port

    def run_server(self):
        pass


class UDPServer(Server):
    pass


class TCPServer(Server):
    pass
