"""Runs the TCP Client sending expressions from file."""

import sys
from time import sleep

from http_suite.bcolors import bcolors
from http_suite.client import TCPClient, parse_expression

if len(sys.argv) > 1:
    filepath = sys.argv[1]
else:
    print("USAGE: python TCP-Client.py [input-file]")
    sys.exit(0)

tc = TCPClient(debug=True)
tc.connect(host="127.0.0.1", port=50123)

# Read file with expressions
with open(filepath) as fp:
    for i, line in enumerate(fp):
        print("\n-------------")
        print(
            "{}{}Reading line #{}.{}\n".format(
                bcolors.WARNING, bcolors.BOLD, i, bcolors.ENDC
            )
        )
        # Remove leading character
        line = line.replace("\n", "")

        tc.http_send(file="/", method="POST", params={"expression": line})

        response = tc.result()

        if response is not False:
            exp = parse_expression(line)
            print(
                "{}{}The result of {} {} {} is {}{}.".format(
                    bcolors.BOLD,
                    bcolors.OKGREEN,
                    exp["a"],
                    exp["op"],
                    exp["b"],
                    response,
                    bcolors.ENDC,
                )
            )
        else:
            print(
                "{}{}Request invalid: there was an error.{}".format(
                    bcolors.BOLD, bcolors.FAIL, bcolors.ENDC
                )
            )

        sleep(1)
