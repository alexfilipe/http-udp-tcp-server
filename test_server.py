from .server import TCPServer

ts = TCPServer(host="127.0.0.1", port=51234)
ts.run()
