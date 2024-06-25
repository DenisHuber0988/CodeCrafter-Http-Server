import pathlib

TRAILING_SLASH = "/"

# Accepted endpoints
BASE_ENDPOINT = ""  # Path '/' when trailing slash is removed -> split("/").
ECHO_ENDPOINT = "echo"
USER_AGENT_ENDPOINT = "user-agent"
FILE_ENDPOINT = "files"

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
    def __init__(self, requested_path: str, headers: list, dirname: str = None):
        """
        :param requested_path: Requested path find in the request.
        :param headers: Headers find in the request. (User-Agent headers for the moment).
        """
        self.requested_path = requested_path
        self.headers = headers
        self.dirname = dirname

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

    def find_path(self) -> tuple[bool, str] | tuple[bool, bytes]:
        endpoint, data = self.extract_endpoint_and_data()

        if endpoint in ENDPOINTS:

            if endpoint == USER_AGENT_ENDPOINT:
                return self.return_version(header=self.headers[0])

            if endpoint == FILE_ENDPOINT:
                return self.return_file(filename=data)

            return True, data

        return False, ""
