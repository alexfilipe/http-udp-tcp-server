"""HTTP Requests and Responses."""

import urllib
from email.utils import formatdate


class Status406(SystemError):
    """Custom exception for HTTP 406 Not Acceptable status."""

    pass


class HTTPRequest:
    """Class for building HTTP requests.

    Args:
        host (str): The host address for the HTTP request. Defaults to "127.0.0.1".
    """

    def __init__(self, host: str = "127.0.0.1"):
        self.http_version = "HTTP/1.1"
        self.server = "calculator/0.1"
        self.host = host
        self.content_type = "text/plain"

        self.post_header_template = (
            "POST {{file}} {http_version}\r\n"
            "Host: {host}\r\n"
            "Content-Type: {content_type}\r\n"
        ).format(
            http_version=self.http_version,
            host=self.host,
            content_type=self.content_type,
        )

        self.get_header_template = (
            "GET {{file}} {http_version}\r\n"
            "Host: {host}\r\n"
            "Content-Type: {content_type}\r\n"
        ).format(
            http_version=self.http_version,
            host=self.host,
            content_type=self.content_type,
        )

    def __build_post(self, params: dict, data: str, file: str) -> str:
        """Build a POST HTTP request.

        Args:
            params (dict): Parameters to include in the request body.
            data (str): Additional data for the request.
            file (str): The file path for the request.

        Returns:
            str: The constructed POST request.
        """
        request = self.post_header_template.format(file=file)

        if params is not None:
            body = urllib.parse.urlencode(params)
            request += "\r\n{}\r\n".format(body)
        else:
            request += "\r\n"

        return request

    def __build_get(self, params: dict, data: str, file: str) -> str:
        """Build a GET HTTP request.

        Args:
            params (dict): Parameters to include in the request body.
            data (str): Additional data for the request.
            file (str): The file path for the request.

        Returns:
            str: The constructed GET request.
        """
        request = self.get_header_template.format(file=file)

        if params is not None:
            body = urllib.parse.urlencode(params)
            request += "\r\n{}\r\n".format(body)
        else:
            request += "\r\n"

        return request

    def build_request(
        self,
        params: dict = None,
        data: str = None,
        file: str = "/",
        method: str = "POST",
    ) -> str:
        """Build an HTTP request.

        Args:
            params (dict): Parameters to include in the request body.
            data (str): Additional data for the request.
            file (str): The file path for the request. Defaults to "/".
            method (str): The HTTP method (POST or GET). Defaults to "POST".

        Returns:
            str: The constructed HTTP request.
        """
        if method == "POST":
            return self.__build_post(file=file, params=params, data=data)
        elif method == "GET":
            return self.__build_get(file=file, params=params, data=data)

        return ""


class HTTPResponse:
    """Class for building HTTP responses."""

    def __init__(self):
        self.http_version = "HTTP/1.1"
        self.status_codes = {200: "200 OK", 406: "406 Not Acceptable"}
        self.content_type = "text/plain"
        self.server = "calculator/0.1"

        self.response_header_template = (
            "{version} {{status}}\r\n"
            "Date: {{date}}\r\n"
            "Content-Type: {content_type}\r\n"
            "Server: {server}\r\n"
            "Connection: close\r\n"
        ).format(
            version=self.http_version,
            server=self.server,
            content_type=self.content_type,
        )

    def __gmt_date(self):
        """Get the current date and time in GMT format.

        Returns:
            str: The current date and time in GMT format.
        """
        return formatdate(timeval=None, localtime=False, usegmt=True)

    def __build_200(self, data: str = None) -> str:
        """Build a 200 OK HTTP response.

        Args:
            data (str): The response body data. Defaults to None.

        Returns:
            str: The constructed 200 OK response.
        """
        response = self.response_header_template.format(
            status=self.status_codes[200], date=self.__gmt_date(), data=data
        )

        if data is not None:
            response += "\r\n{}\r\n".format(data)
        else:
            response += "\r\n"

        return response

    def __build_406(self, data: str = None) -> str:
        """Build a 406 Not Acceptable HTTP response.

        Args:
            data (str): The response body data. Defaults to None.

        Returns:
            str: The constructed 406 Not Acceptable response.
        """
        response = self.response_header_template.format(
            status=self.status_codes[406], date=self.__gmt_date(), data=data
        )

        if data is not None:
            response += "\r\n{}\r\n".format(data)
        else:
            response += "\r\n"

        return response

    def build_response(self, data: str = None, status: int = 200) -> str:
        """Build an HTTP response.

        Args:
            data (str): The response body data. Defaults to None.
            status (int): The HTTP status code. Defaults to 200.

        Returns:
            str: The constructed HTTP response.
        """
        response = ""

        if status == 200:
            response = self.__build_200(data)
        elif status == 406:
            response = self.__build_406(data)

        return response


class HTTPParser:
    """Class to parse HTTP responses and requests."""

    def get_header_fields(self, response: str) -> dict:
        """Extract header fields from an HTTP message.

        Args:
            response (str): The HTTP message.

        Returns:
            dict: A dictionary of header fields and their values.
        """
        fields = {}

        for line in response.splitlines()[1:]:
            if line == "":
                break

            split_line = line.split(":", 1)
            field = split_line[0].strip()
            fields[field] = split_line[1].strip()

        return fields

    def get_contents(self, response: str) -> str:
        """Extract the body content from an HTTP message.

        Args:
            response (str): The HTTP message.

        Returns:
            str: The body content of the message.
        """
        split_response = response.split("\r\n\r\n", 1)

        if len(split_response) == 1:
            return ""

        return split_response[1].rstrip()

    def get_status_code(self, response: str) -> int:
        """Extract the status code from an HTTP response.

        Args:
            response (str): The HTTP response.

        Returns:
            int: The status code.
        """
        first_line = response.splitlines()[0]
        status_code = int(first_line.split(" ")[1])
        return status_code

    def parse_response(self, response: str) -> dict:
        """Parse an HTTP response into its components.

        Args:
            response (str): The HTTP response.

        Returns:
            dict: A dictionary containing the status, fields, and data.
        """
        return {
            "status": self.get_status_code(response),
            "fields": self.get_header_fields(response),
            "data": self.get_contents(response),
        }

    def get_params(self, request: str) -> dict:
        """Extract parameters from a POST HTTP request.

        Args:
            request (str): The HTTP request.

        Returns:
            dict: A dictionary of parameters.
        """
        params = self.get_contents(request)

        if params:
            return urllib.parse.parse_qs(params)

        return {}

    def get_method(self, request: str) -> str:
        """Extract the HTTP method from a request.

        Args:
            request (str): The HTTP request.

        Returns:
            str: The HTTP method (e.g., GET, POST).
        """
        return request.splitlines()[0].split(" ")[0]

    def get_filename(self, request: str) -> str:
        """Extract the file path from an HTTP request.

        Args:
            request (str): The HTTP request.

        Returns:
            str: The file path.
        """
        return request.splitlines()[0].split(" ")[1]

    def parse_request(self, request: str) -> dict:
        """Parse an HTTP request into its components.

        Args:
            request (str): The HTTP request.

        Returns:
            dict: A dictionary containing the method, fields, file, and params.
        """
        try:
            return {
                "method": self.get_method(request),
                "fields": self.get_header_fields(request),
                "file": self.get_filename(request),
                "params": self.get_params(request),
            }
        except Exception:
            return False
