import pathlib

# Accepted endpoints
BASE_ENDPOINT = {"": ["GET"]}  # Path '/' when trailing slash is removed -> split("/").
ECHO_ENDPOINT = {"echo": ["GET"]}
USER_AGENT_ENDPOINT = {"user-agent": ["GET"]}
FILE_ENDPOINT = {"files": ["GET", "POST"]}

ENDPOINTS = [
    BASE_ENDPOINT,
    ECHO_ENDPOINT,
    USER_AGENT_ENDPOINT,
    FILE_ENDPOINT
]


class Path:
    """
    Check that the requested path exists, and do the right action
    """
    def __init__(self, headers: dict, dirname: str,):
        """
        :param headers: Contains all the information to process the response.
        {
            'HTTP_METHOD': 'GET',
            'HTTP_PATH': '/echo/abc',
            'HTTP_VERSION': 'HTTP/1.1',
            'User-Agent:': 'User-Agent: curl/7.81.0',
            'HTTP_ENCODING_HEADER': ['gzip'],$
            'REQUEST_DATA': None
        }

        :param dirname: The directory name to find or create a file.
        """
        self.headers = headers
        self.dirname = dirname

    def return_version(self) -> tuple[bool, str]:
        # Return the version of the product (User-Agent)
        if self.headers.get("USER_AGENT_HEADER", None):
            try:
                _, version = self.headers["USER_AGENT_HEADER"].split(" ")
            except ValueError:
                version = self.headers["USER_AGENT_HEADER"].split(" ")[0]

            return True, version

        return False, ""

    def return_file(self, filename) -> tuple[bool, str] | tuple[bool, bytes]:
        if self.dirname is None or filename is None:
            return False, ""

        file = pathlib.Path(self.dirname, filename).resolve()
        if file.is_file():
            return True, file.read_bytes()

        return False, ""

    def get(self, endpoint) -> tuple[bool, str] | tuple[bool, bytes]:
        data = self.headers["HTTP_PATH_DATA"]

        if any(ENDPOINT.get(endpoint, None) for ENDPOINT in ENDPOINTS):
            if endpoint in USER_AGENT_ENDPOINT.keys():
                return self.return_version()
            if endpoint in FILE_ENDPOINT.keys():
                return self.return_file(filename=data)

            return True, data

        return False, ""

    def post(self, endpoint) -> tuple[bool, str] | tuple[bool, bytes]:
        filename = self.headers["HTTP_PATH_DATA"]

        if endpoint not in FILE_ENDPOINT.keys():
            return False, ""

        with pathlib.Path(self.dirname, filename) as file:
            data = self.headers['REQUEST_DATA']
            file.write_bytes(data.encode())

        return True, data.encode()

    def find_path(self) -> tuple[bool, str] | tuple[bool, bytes]:
        """
        Check that the path sent in the request is registered in ENDPOINTS.
        """
        handler = getattr(self, self.headers.get("HTTP_METHOD", "").lower(), None)

        if handler is not None:
            return handler(endpoint=self.headers["HTTP_PATH"])

        return False, ""
