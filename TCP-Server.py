import sys
from server import TCPServer
from calc import Calculator

ts = TCPServer(host="127.0.0.1", port=50123)
ts.run()
