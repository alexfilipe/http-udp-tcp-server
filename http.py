"""HTTP Requests and Responses."""

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

        self.post_template = (
            "POST {{file}} {http_version}\n"
            "Host: {host}\n"
            "Content-Type: {content_type}\n"
            "\n{{data}}"
        )

        self.post_template = self.post_template.format(
            http_version=self.http_version,
            host=self.host,
            content_type=self.content_type
        )


    def __build_post(self, params: dict, file: str) -> str:
        """Build POST request with parameters."""
        if params is None:
            params = {}

        body = urllib.parse.urlencode(params)

        request = self.post_template.format(
            file=file,
            data=body
        )

        return request


    def __build_get(self, params: dict, data: str, file: str) -> str:
        raise NotImplementedError


    def build_request(self, params: dict=None, data: str=None,
                      file: str="/", method: str="POST") -> str:
        """Build HTTP request with data and parameters."""

        if params is None:
            params = {}

        if method == "POST":
            return self.__build_post(file=file, params=params)
        elif method == "GET":
            return self.__build_get(file=file, data=data)

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

        self.response_template = (
            "{version} {{status}}\n"
            "Date: {{date}}\n"
            "Content-Type: {content_type}\n"
            "Server: {server}\n"
            "\n{{data}}"
        )

        self.response_template = self.response_template.format(
            version=self.http_version,
            server=self.server,
            content_type=self.content_type
        )

    def __gmt_date(self):
        """Return current datetime in GMT format."""
        return formatdate(timeval=None, localtime=False, usegmt=True)

    def __build_200(self, data: str=None) -> str:
        """Build 200 OK response."""
        if data is None:
            data = ""

        response = self.response_template.format(
            status=self.status_codes[200],
            date=self.__gmt_date(),
            data=data
        )

        return response

    def __build_406(self, data: str=None) -> str:
        """Build 406 Not Acceptable response."""
        if data is None:
            data = ""

        response = self.response_template.format(
            status=self.status_codes[406],
            date=self.__gmt_date(),
            data=data
        )

        return response

    def build_response(self, data: str=None, status: int=200) -> str:
        """Build the HTTP response."""
        response = ""

        if status == 200:
            response = self.__build_200(data)
        elif status == 406:
            response = self.__build_406(data)

        return response