from http_suite.server import TCPServer

ts = TCPServer(host="127.0.0.1", port=50123)
ts.run()
