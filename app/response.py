from app.constant import CRLF


class Response:
    """
    Http response with status and headers.
    """

    # Headers for the response.
    CONTENT_TYPE_HEADER = "Content-Type:"
    CONTENT_LENGTH_HEADER = "Content-Length:"
    USER_AGENT_HEADER = "User-Agent:"
    ACCEPT_HEADER = "Accept:"

    def __init__(self, data, http_version, status_code):
        self.data = data
        self.http_version = http_version
        self.status_code = status_code

    def get_status_line(self):
        code, reason = self.status_code
        return " ".join([self.http_version, code, reason])

    def get_content_type(self):
        content_type = ""

        if isinstance(self.data, (str, int)):
            content_type = "text/plain"
        elif isinstance(self.data, bytes):
            content_type = "application/octet-stream"
            self.data = self.data.decode()

        return "".join([self.CONTENT_TYPE_HEADER, content_type])

    def get_content_length(self):
        content_length = len(self.data)
        return " ".join([self.CONTENT_LENGTH_HEADER, str(content_length)])

    def render_response(self):
        status_line = self.get_status_line()
        content_type = self.get_content_type()
        content_length = self.get_content_length()
        body = ""

        components = [status_line, content_type, content_length, body, self.data]
        response = CRLF.join([component for component in components])

        return response.encode()
