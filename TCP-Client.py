"""Runs the TCP Client sending expressions from file."""
import sys
from client import TCPClient
from http import HTTPRequest, HTTPParser

if len(sys.argv) > 1:
    filepath = sys.argv[1]
else:
    filepath = "expressions.txt"

tc = TCPClient()
tc.connect(host="127.0.0.1", port=50123)

# Read file with expressions
with open(filepath) as fp:
    for line in fp:
        # Remove leading character
        line = line.replace("\n", "")

        print("Sending HTTP Request...")
        tc.http_send(
            file="/",
            method="POST",
            params={"expression": line}
        )

        response = tc.receive()

        print("Response:")
        print(response.decode())
