from server import UDPReliableServer

us = UDPReliableServer(host="127.0.0.1",
                       server_port=50123,
                       client_port=50321)
us.run()
