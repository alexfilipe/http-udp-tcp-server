from http import HTTPRequest, HTTPResponse

http_req = HTTPRequest(host="127.0.0.1")

print(http_req.build_request(
    method="POST",
    params={
        "expression": "+ 1 2"
    }
), "\n")

http_resp = HTTPResponse()

print(http_resp.build_response(status=406,
                               data=-1), "\n")

print(http_resp.build_response(status=200,
                               data='10'))
