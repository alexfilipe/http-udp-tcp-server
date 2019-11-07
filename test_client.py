from client import TCPClient

tc = TCPClient()

tc.connect(host="127.0.0.1", port=50123)

tc.send("hello")
print(tc.receive())
