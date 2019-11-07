from http import HTTPRequest, HTTPResponse, HTTPParser

http_parser = HTTPParser()

http_req = HTTPRequest(host="127.0.0.1")

print(http_req.build_request(
    method="POST",
    params={"expression": "+ 1 2"}
), "\n")

request1 = http_req.build_request(
    method="POST",
    file="/testfilename",
    params={"expression": "* 5 6"}
)

print("Request 1:")
print(request1)
print("Parsed request:", http_parser.parse_request(request1))

http_resp = HTTPResponse()

response1 = http_resp.build_response(status=406, data=-1)
parsed_response1 = http_parser.parse_response(response1)
print()

print("Response 1:")
print(response1, "\n")
print("Status:", parsed_response1['status'])
print("Header Fields:", parsed_response1['fields'])
print("Data:", parsed_response1['data'])


response2 = http_resp.build_response(status=200, data="10")
parsed_response2 = http_parser.parse_response(response2)
print()

print("Response 2:")
print(response2, "\n")
print("Status:", parsed_response2['status'])
print("Header Fields:", parsed_response2['fields'])
print("Data:", parsed_response2['data'])

response3 = http_resp.build_response(status=406)
parsed_response3 = http_parser.parse_response(response3)
print()

print("Response 3:")
print(response3, "\n")
print("Status:", parsed_response3['status'])
print("Header Fields:", parsed_response3['fields'])
print("Data:", parsed_response3['data'])
