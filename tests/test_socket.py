import socket

from http_suite.http import HTTPRequest

server = "www.inspirasonho.com.br"
file = "/sobre"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((server, 80))

hreq = HTTPRequest(host=server)
request = hreq.build_request(method="GET", file=file)

print("Request:")
print(request)
print("----\n")


s.send(request.encode())

response = s.recv(4096)

print("Response:")
print(response.decode())
print()
print("Response Length:", len(response))
