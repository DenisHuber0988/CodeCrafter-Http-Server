import pathlib

TRAILING_SLASH = "/"

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
    def __init__(self, method: str, requested_path: str, headers: list, dirname: str, body: str):
        """
        :param method: GET or POST method.
        :param requested_path: Requested path find in the request.
        :param headers: Headers find in the request. (User-Agent headers for the moment).
        :param dirname: The directory name to find or create a file.
        :param body: The data to write into a file.
        """
        self.method = method
        self.requested_path = requested_path
        self.headers = headers
        self.dirname = dirname
        self.body = body

    @staticmethod
    def return_version(header: str) -> tuple[bool, str]:
        # Return the version of the product (User-Agent)
        _, version = header.split(" ")
        return True, version

    def return_file(self, filename) -> tuple[bool, str] | tuple[bool, bytes]:
        if self.dirname is None or filename is None:
            return False, ""

        file = pathlib.Path(self.dirname, filename).resolve()
        if file.is_file():
            return True, file.read_bytes()

        return False, ""

    def extract_endpoint_and_data(self) -> tuple[str, str]:
        try:
            _, endpoint, data = self.requested_path.split(TRAILING_SLASH)
        except ValueError:  # There is no data in the request.
            _, endpoint = self.requested_path.split(TRAILING_SLASH)
            data = ""

        return endpoint, data

    def get(self, endpoint, data) -> tuple[bool, str] | tuple[bool, bytes]:
        if any(ENDPOINT.get(endpoint, None) for ENDPOINT in ENDPOINTS):
            if endpoint in USER_AGENT_ENDPOINT.keys():
                return self.return_version(header=self.headers[0])
            if endpoint in FILE_ENDPOINT.keys():
                return self.return_file(filename=data)

            return True, data

        return False, ""

    def post(self, endpoint, filename) -> tuple[bool, str] | tuple[bool, bytes]:
        if endpoint not in FILE_ENDPOINT.keys():
            return False, ""

        with pathlib.Path(self.dirname, filename) as file:
            file.write_bytes(self.body.encode())

        return True, self.body.encode()

    def find_path(self) -> tuple[bool, str] | tuple[bool, bytes]:
        """
        Check that the path sent in the request is registered in ENDPOINTS.
        """
        endpoint, data = self.extract_endpoint_and_data()
        handler = getattr(self, self.method.lower(), None)

        if handler is not None:
            return handler(endpoint, data)

        return False, ""
