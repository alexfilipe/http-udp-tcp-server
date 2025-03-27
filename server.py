"""TCP/UDP Calculator Servers."""

import random
import socket
import sys

from .bcolors import bcolors
from .calc import Calculator
from .http import HTTPParser, HTTPResponse


class Server:
    """UDP/TCP server with Sockets."""

    def __init__(
        self, host: str = "127.0.0.1", port: int = 50123, buffer_size: int = 1024
    ):
        self.host = host
        self.port = port
        self.buffer_size = buffer_size

        self.server_socket.bind((host, port))

    def process_request(self, message: str) -> str:
        """Processes HTTP request and returns response."""
        parser = HTTPParser()
        response = HTTPResponse()
        calc = Calculator()

        request = parser.parse_request(message)

        # Invalid request (no expression sent)
        if not request["params"] or "expression" not in request["params"]:

            print("Request is invalid. Missing parameters.")
            return response.build_response(status=406, data="-1")

        expression = request["params"]["expression"][0]
        print(
            "{}Expression received:{} {}".format(
                bcolors.OKBLUE, bcolors.ENDC, expression
            )
        )

        # Evaluate the expression
        try:
            result = calc.evaluate(expression)
            print(
                "{}Expression valid{}, result = {}".format(
                    bcolors.OKGREEN, bcolors.ENDC, result
                )
            )

            return response.build_response(status=200, data=result)

        # Send error message if not valid
        except Exception as exc:
            print(
                "{}An exception occurred:{} {} ({})".format(
                    bcolors.FAIL, bcolors.ENDC, str(exc), type(exc).__name__
                )
            )

            return response.build_response(status=406, data="-1")

        return ""

    def run(self):
        raise NotImplementedError


class TCPServer(Server):
    """Reliable TCP Server."""

    def __init__(
        self, host: str = "127.0.0.1", port: int = 50123, buffer_size: int = 1024
    ):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        super().__init__(host, port, buffer_size)

    def run(self):
        """Runs server until Control+C is called."""

        print(
            "{}{}TCP server started.{}".format(
                bcolors.BOLD, bcolors.OKGREEN, bcolors.ENDC
            )
        )
        try:
            while True:
                self.server_socket.listen(1)
                client_socket, address = self.server_socket.accept()

                connected = True

                while connected:
                    data = client_socket.recv(self.buffer_size)

                    if data:
                        print("----------------")
                        print(
                            "{}{}Received packet. Data:{}\n{}".format(
                                bcolors.BOLD,
                                bcolors.OKBLUE,
                                bcolors.ENDC,
                                data.decode(),
                            )
                        )

                        response = self.process_request(data.decode())

                        print(
                            "\n{}{}Sending response. Data:{}\n{}".format(
                                bcolors.BOLD, bcolors.OKBLUE, bcolors.ENDC, response
                            )
                        )

                        client_socket.send(response.encode())

                    else:
                        print("----------------")
                        print(
                            "{}{}Connection ended.{}".format(
                                bcolors.BOLD, bcolors.WARNING, bcolors.ENDC
                            )
                        )
                        connected = False
                        client_socket.close()

        except KeyboardInterrupt:
            print("----------------")
            print(
                "{}{}Server aborted.{}".format(
                    bcolors.BOLD, bcolors.WARNING, bcolors.ENDC
                )
            )
            self.server_socket.close()
            sys.exit(0)


class UDPReliableServer(Server):
    """UDP Server running on reliable environment."""

    def __init__(
        self, host: str = "127.0.0.1", port: int = 50123, buffer_size: int = 1024
    ):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        super().__init__(host=host, port=port, buffer_size=buffer_size)

    def run(self):
        """Runs server until Control+C is called."""

        print(
            "{}{}UDP server started.{}".format(
                bcolors.BOLD, bcolors.OKGREEN, bcolors.ENDC
            )
        )
        try:
            while True:
                data, addr = self.server_socket.recvfrom(self.buffer_size)

                print("Address:", addr)

                if data:
                    print("----------------")
                    print(
                        "{}{}Received packet. Data:{}\n{}".format(
                            bcolors.BOLD, bcolors.OKBLUE, bcolors.ENDC, data.decode()
                        )
                    )

                    response = self.process_request(data.decode())

                    print(
                        "\n{}{}Sending response. Data:{}\n{}".format(
                            bcolors.BOLD, bcolors.OKBLUE, bcolors.ENDC, response
                        )
                    )

                    self.server_socket.sendto(response.encode(), (self.host, addr[1]))

        except KeyboardInterrupt:
            print("----------------")
            print(
                "{}{}Server aborted.{}".format(
                    bcolors.BOLD, bcolors.WARNING, bcolors.ENDC
                )
            )
            self.server_socket.close()
            sys.exit(0)


class UDPUnreliableServer(UDPReliableServer):
    """UDP Server running on unreliable environment.
    This server drops a received UDP packet with a certain probability."""

    def __init__(
        self,
        host: str = "127.0.0.1",
        port: int = 50123,
        buffer_size: int = 1024,
        prob_drop=0.75,
    ):
        """prob_drop: probability of a packet being dropped"""

        self.prob_drop = prob_drop
        super().__init__(host=host, port=port, buffer_size=buffer_size)

    def run(self):
        """Runs server until Control+C is called."""

        print(
            "{}{}UDP server started.{}".format(
                bcolors.BOLD, bcolors.OKGREEN, bcolors.ENDC
            )
        )

        # Run server until Ctrl+C is pressed."""
        try:
            while True:
                data, addr = self.server_socket.recvfrom(self.buffer_size)

                # Drop packet with a given probability
                if random.random() >= self.prob_drop:
                    print("----------------")
                    print(
                        "{}{}Received packet. Data:{}\n{}".format(
                            bcolors.BOLD, bcolors.OKBLUE, bcolors.ENDC, data.decode()
                        )
                    )

                    response = self.process_request(data.decode())

                    print(
                        "\n{}{}Sending response. Data:{}\n{}".format(
                            bcolors.BOLD, bcolors.OKBLUE, bcolors.ENDC, response
                        )
                    )

                    self.server_socket.sendto(response.encode(), (self.host, addr[1]))
                else:
                    print("----------------")
                    print(
                        "{}{}Packet received, but dropped.{}\n".format(
                            bcolors.BOLD, bcolors.FAIL, bcolors.ENDC
                        )
                    )

        except KeyboardInterrupt:
            print("----------------")
            print(
                "{}{}Server aborted.{}".format(
                    bcolors.BOLD, bcolors.WARNING, bcolors.ENDC
                )
            )
            self.server_socket.close()
            sys.exit(0)
