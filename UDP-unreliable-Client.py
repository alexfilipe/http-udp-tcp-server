"""Runs the UDP Unreliable Client sending expressions from file."""
import sys
from bcolors import bcolors
from client import parse_expression, UDPUnreliableClient, TimeoutException
from time import sleep

if len(sys.argv) > 1:
    filepath = sys.argv[1]
else:
    filepath = "expressions.txt"

uuc = UDPUnreliableClient(debug=True,
                          server_port=50321,
                          server_addr="127.0.0.1")

# Read file with expressions
with open(filepath) as fp:
    for i, line in enumerate(fp):
        print("\n-------------")
        print("{}{}Reading line #{}.{}\n".format(
              bcolors.WARNING, bcolors.BOLD, i, bcolors.ENDC))
        # Remove leading character
        line = line.replace("\n", "")

        try:
          response = uuc.http_req(
              host="127.0.0.1",
              port=50123,
              file="/",
              method="POST",
              params={"expression": line}
          )
        except TimeoutException:
          print("{}{}Timeout exceeded for this operation.{}".format(
                bcolors.BOLD, bcolors.FAIL, bcolors.ENDC))
          continue

        if response is not False:
            exp = parse_expression(line)
            print("{}{}The result of {} {} {} is {}{}."
                  .format(bcolors.BOLD, bcolors.OKGREEN,
                          exp["a"], exp["op"], exp["b"],
                          response, bcolors.ENDC))
            packet_received = True
        else:
            print("{}{}Request invalid: there was an error.{}"
                  .format(bcolors.BOLD, bcolors.FAIL,
                          bcolors.ENDC))
            packet_received = True

        sleep(2)
