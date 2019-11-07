"""HTTP Requests and Responses."""
import re
import urllib
from email.utils import formatdate

class Status406(SystemError):
    pass


class HTTPRequest:
    """Class for building HTTP requests."""

    def __init__(self, host: str="127.0.0.1"):
        self.http_version = "HTTP/1.1"

        self.server = "calculator/0.1"

        self.host = host

        self.content_type = "text/plain"

        self.post_header_template = (
            "POST {{file}} {http_version}\r\n"
            "Host: {host}\r\n"
            "Content-Type: {content_type}\r\n"
        )

        self.post_header_template = self.post_header_template.format(
            http_version=self.http_version,
            host=self.host,
            content_type=self.content_type
        )

        self.get_header_template = (
            "GET {{file}} {http_version}\r\n"
            "Host: {host}\r\n"
            "Content-Type: {content_type}\r\n"
        )

        self.get_header_template = self.get_header_template.format(
            http_version=self.http_version,
            host=self.host,
            content_type=self.content_type
        )

    def __build_post(self, params: dict, data: str, file: str) -> str:
        """Build POST request with parameters."""
        request = self.post_header_template.format(file=file)

        if params is not None:
            body = urllib.parse.urlencode(params)
            request += "\r\n{}\r\n".format(body)
        else:
            request += "\r\n"

        return request


    def __build_get(self, params: dict, data: str, file: str) -> str:
        request = self.get_header_template.format(file=file)

        if params is not None:
            body = urllib.parse.urlencode(params)
            request += "\r\n{}\r\n".format(body)
        else:
            request += "\r\n"

        return request


    def build_request(self, params: dict=None, data: str=None,
                      file: str="/", method: str="POST") -> str:
        """Build HTTP request with data and parameters."""
        if method == "POST":
            return self.__build_post(file=file, params=params, data=data)
        elif method == "GET":
            return self.__build_get(file=file, params=params, data=data)

        return ""


class HTTPResponse:
    """Class for building HTTP responses."""

    def __init__(self):
        self.http_version = "HTTP/1.1"

        self.status_codes = {
            200: "200 OK",
            406: "406 Not Acceptable"
        }

        self.content_type = "text/plain"

        self.server = "calculator/0.1"

        self.response_header_template = (
            "{version} {{status}}\r\n"
            "Date: {{date}}\r\n"
            "Content-Type: {content_type}\r\n"
            "Server: {server}\r\n"
        )

        self.response_header_template = self.response_header_template.format(
            version=self.http_version,
            server=self.server,
            content_type=self.content_type
        )


    def __gmt_date(self):
        """Return current datetime in GMT format."""

        return formatdate(timeval=None, localtime=False, usegmt=True)


    def __build_200(self, data: str=None) -> str:
        """Build 200 OK response."""

        response = self.response_header_template.format(
            status=self.status_codes[200],
            date=self.__gmt_date(),
            data=data
        )

        if data is not None:
            response += "\r\n{}\r\n".format(data)
        else:
            response += "\r\n"

        return response


    def __build_406(self, data: str=None) -> str:
        """Build 406 Not Acceptable response."""
        response = self.response_header_template.format(
            status=self.status_codes[406],
            date=self.__gmt_date(),
            data=data
        )

        if data is not None:
            response += "\r\n{}\r\n".format(data)
        else:
            response += "\r\n"

        return response


    def build_response(self, data: str=None, status: int=200) -> str:
        """Build the HTTP response."""
        response = ""

        if status == 200:
            response = self.__build_200(data)
        elif status == 406:
            response = self.__build_406(data)

        return response


class HTTPParser:
    """Class to parse HTTP Responses."""

    def get_header_fields(self, response: str) -> dict:
        fields = {}

        for line in response.splitlines()[1:]:
            if line == "":
                break

            split_line = line.split(" ", 1)
            field = split_line[0][:-1]
            fields[field] = split_line[1]

        return fields

    def get_contents(self, response: str) -> dict:
        split_response = response.split("\n\n", 1)

        if len(split_response) == 1:
            return ""

        return split_response[1]

    def get_status_code(self, response: str) -> int:
        first_line = response.splitlines()[0]
        status_code = int(first_line.split(" ")[1])
        return status_code

    def parse_response(self, response: str) -> dict:
        return {
            "status": self.get_status_code(response),
            "fields": self.get_header_fields(response),
            "data": self.get_contents(response),
        }

    def get_params(self, request: str) -> dict:
        params = self.get_contents(request)

        if params:
            return urllib.parse.parse_qs(params)

        return {}

    def get_method(self, request: str) -> str:
        return request.splitlines()[0].split(" ")[0]

    def get_filename(self, request: str) -> str:
        return request.splitlines()[0].split(" ")[1]

    def parse_request(self, request: str) -> dict:
        return {
            "method": self.get_method(request),
            "fields": self.get_header_fields(request),
            "file": self.get_filename(request),
            "params": self.get_params(request)
        }
