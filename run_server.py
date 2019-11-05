from http import HTTPRequest, HTTPResponse
from calc import Calculator

http_req = HTTPRequest(host="127.0.0.1")
http_resp = HTTPResponse()
calc = Calculator()

exp = ""
while True:
    print("Type in your expression: ", end="")
    exp = input()

    print()

    if exp == "exit":
        break

    request = http_req.build_request(method="POST", params={
        "expression": exp
    })

    print("Making HTTP request...")
    print("----------------------")
    print(request, "\n")

    print("Evaluating expression...")
    print("------------------------")

    try:
        result = calc.evaluate(exp)

        print("Calculation result:", result, "\n")

        print("Retrieving HTTP response...")
        print("---------------------------")

        response = http_resp.build_response(status=200, data=result)
        print(response, "\n")

    except Exception as ex:
        print("An exception occurred: {} ({}).".format(
            str(ex), type(ex).__name__
        ), "\n")

        print("Retrieving HTTP response...")
        print("---------------------------")

        response = http_resp.build_response(status=406, data=-1)
        print(response, "\n")
