from server import UDPUnreliableServer
from bcolors import bcolors

print("{}{}Type in probability of dropping a packet: {}".
      format(bcolors.BOLD, bcolors.OKBLUE, bcolors.ENDC), end="")
prob_drop = float(input())

us = UDPUnreliableServer(host="127.0.0.1",
                         server_port=50123,
                         client_port=50321,
                         prob_drop=prob_drop)
us.run()
