from server import UDPReliableServer

us = UDPReliableServer(host="127.0.0.1", port=50123)
us.run()
