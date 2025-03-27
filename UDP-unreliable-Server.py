import sys

from .server import UDPUnreliableServer

if len(sys.argv) > 1:
    prob_drop = float(sys.argv[1])
else:
    print(
        "USAGE: python UDP-unreliable-Server.py [probability]\n"
        "    where [probability] is a float between 0.0 and 1.0\n"
        "    representing the probability of dropping a packet"
    )
    sys.exit(0)

us = UDPUnreliableServer(host="127.0.0.1", port=50123, prob_drop=prob_drop)
us.run()
