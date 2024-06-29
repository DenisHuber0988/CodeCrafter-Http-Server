import copy
import gzip

from app.constant import CRLF
from app.utils import remove_none_elements_from_list


class Response:
    """
    Initialize response with status and headers.
    """

    # Header from the request.
    ACCEPT_ENCODING_HEADER = "Accept-Encoding:"

    # Headers for the response.
    CONTENT_TYPE_HEADER = "Content-Type:"
    CONTENT_LENGTH_HEADER = "Content-Length:"
    CONTENT_ENCODING_HEADER = "Content-Encoding:"

    # List of valid encoding for the CONTENT_ENCODING_HEADER
    SUPPORTED_ENCODING_TYPE = ["gzip"]
    INVALID_SUFFIX = "invalid-"

    def __init__(self, data: str, content_type: str, status_code: tuple, headers: dict):
        """

        :param data: The data to return to the client.
        :param content_type: The content_type to return in the CONTENT_TYPE_HEADER.
        :param status_code: The status of the response.
        :param headers: Information received on the request.
        """
        self.data = data.encode()
        self.content_type = content_type
        self.status_code = status_code
        self.headers = headers

    def get_status_line(self):
        code, reason = self.status_code
        return " ".join([self.headers["HTTP_VERSION"], code, reason])

    def get_content_type(self):
        return " ".join([self.CONTENT_TYPE_HEADER, self.content_type])

    def get_content_length(self):
        content_length = len(self.data)
        return " ".join([self.CONTENT_LENGTH_HEADER, str(content_length)])

    def get_content_encoding(self):
        content_encoding_type = copy.copy(self.headers.get("HTTP_ENCODING_HEADER", None))

        if any(encoding in self.SUPPORTED_ENCODING_TYPE for encoding in self.headers.get("HTTP_ENCODING_HEADER", None)):
            # Find the supported encoding type.
            for encoding_type in self.headers.get("HTTP_ENCODING_HEADER", None):
                if encoding_type not in self.SUPPORTED_ENCODING_TYPE:
                    content_encoding_type.remove(encoding_type)

            encoding_type = None if content_encoding_type == [] else content_encoding_type[0]
            return " ".join([self.CONTENT_ENCODING_HEADER, encoding_type])

    def render_response(self):
        status_line = self.get_status_line()
        content_type = self.get_content_type()
        content_encoding = self.get_content_encoding()

        if content_encoding and "gzip" in content_encoding:
            self.data = gzip.compress(self.data)

        content_length = self.get_content_length()

        crlf = CRLF.encode()
        response_content = remove_none_elements_from_list([
            status_line, content_type, content_length, content_encoding, ""]
        )
        response = CRLF.join([content for content in response_content])

        response = crlf.join([response.encode(), self.data, b""])
        return response

