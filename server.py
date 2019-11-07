"""TCP/UDP Calculator Servers."""

from calc import (Calculator, OperationIncomplete,
                  InvalidOperation, NotAnInteger)
from http import HTTPResponse, HTTPParser
import socket
from bcolors import bcolors

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

    def process_request(self, message: str) -> str:
        """Processes HTTP request and returns response."""
        parser = HTTPParser()
        response = HTTPResponse()
        calc = Calculator()

        request = parser.parse_request(message)

        # Invalid request (no expression sent)
        if (not request["params"]
            or "expression" not in request["params"]):

            print("Request is invalid. Missing parameters.")
            return response.build_response(status=406, data="-1")

        expression = request["params"]["expression"][0]
        print("{}Expression received:{} {}".format(bcolors.OKBLUE,
                                                   bcolors.ENDC,
                                                   expression))

        # Evaluate the expression
        try:
            result = calc.evaluate(expression)
            print("{}Expression valid{}, result = {}".format(bcolors.OKGREEN,
                                                             bcolors.ENDC,
                                                             result))

            return response.build_response(status=200, data=result)

        # Send error message if not valid
        except Exception as exc:
            print("{}An exception occurred:{} {} ({})"
                  .format(bcolors.FAIL, bcolors.ENDC,
                          str(exc), type(exc).__name__))

            return response.build_response(status=406, data="-1")

        return ""


    def run(self):
        raise NotImplementedError


class TCPServer(Server):
    """Reliable TCP Server."""

    def run(self):
        """Runs server until Control+C is called."""

        print("{}{}TCP server started.{}".format(bcolors.BOLD,
                                                 bcolors.OKGREEN,
                                                 bcolors.ENDC))

        client_socket, address = self.server_socket.accept()

        while True:
            data = client_socket.recv(self.buffer_size)

            if data:
                print("----------------")
                print("{}{}Received packet. Data:{}\n{}".format(bcolors.BOLD,
                                                                bcolors.OKBLUE,
                                                                bcolors.ENDC,
                                                                data.decode()))

                response = self.process_request(data.decode())

                print("\n{}{}Sending response. Data:{}\n{}".format(
                      bcolors.BOLD, bcolors.OKBLUE, bcolors.ENDC, response))
                client_socket.send(response.encode())
            else:
                print("----------------")
                print("{}{}Connection ended.{}".format(bcolors.BOLD,
                                                       bcolors.WARNING,
                                                       bcolors.ENDC))
                break

        client_socket.close()


class UDPReliableServer(Server):
    """UDP Server running on reliable environment."""
    pass


class UDPUnreliableServer(Server):
    """UDP Server running on unreliable environment."""
    pass
