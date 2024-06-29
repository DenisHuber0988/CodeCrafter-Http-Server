from app import status_code
from app.constant import CRLF
from app.paths import Path
from app.response import Response


class Parser:
    """
    Parse the incoming request from the Server, and return a constructed Response.
    """

    USER_AGENT_HEADER = "User-Agent:"
    ACCEPT_HEADER = "Accept:"

    def __init__(self, request, dirname):
        """
        :param request: The request sent by the client.
        :param dirname: The directory name from where to read a file.
        """
        self.request = request
        self.dirname = dirname

    def get_request_header(self) -> dict:
        """
        Parse the first part of the request with Method - Path - Http-Version.
        """
        request_header = self.request.split(CRLF)[0]
        method, requested_path, http_version = request_header.split()
        # Remove trailing_slash
        try:
            path, data = requested_path.lstrip("/").split("/")
        except ValueError:
            path = requested_path.lstrip("/").split("/")[0]
            data = ""

        request_header_dict = {
            "HTTP_METHOD": method,
            "HTTP_PATH_DATA": data,
            "HTTP_PATH": path,
            "HTTP_VERSION": http_version
        }
        return request_header_dict

    def get_user_agent_header(self) -> dict:
        """
        Parse the User-Agent: header from the request.
        """
        user_agent_header = {"USER_AGENT_HEADER": None}
        for header in self.request.split(CRLF):
            if header.startswith(self.USER_AGENT_HEADER):
                user_agent_header["USER_AGENT_HEADER"] = header.split(" ")[1]
                return user_agent_header

        return user_agent_header

    def get_accept_header(self) -> dict:
        """
        Parse the Accept: header from the request.
        """
        accept_header = {self.ACCEPT_HEADER: None}
        for header in self.request.split(CRLF):
            if header.startswith(self.ACCEPT_HEADER):
                accept_header[self.ACCEPT_HEADER] = header
                return header

        return accept_header

    def fetch_data(self, headers) -> dict:
        """
        In a POST scenario, the data/body to process are found at the end of the request.
        """
        data_header = {"REQUEST_DATA": None}
        if headers.get("HTTP_METHOD") == "POST":
            data_header["REQUEST_DATA"] = self.request.split(CRLF)[-1]

        return data_header

    def get_encoding_header(self) -> dict:
        """
        Parse the request and try to find the Accept-Encoding header.
        """
        encoding_header = {"HTTP_ENCODING_HEADER": []}
        for header in self.request.split(CRLF):
            if header.startswith(Response.ACCEPT_ENCODING_HEADER):
                encoding_type = header.split(": ")[-1]
                encoding_header["HTTP_ENCODING_HEADER"] = encoding_type.split(", ")
                return encoding_header

        return encoding_header

    def check_path(self, headers) -> Response:
        body = self.fetch_data(headers=headers)
        headers.update(body)

        path = Path(headers=headers, dirname=self.dirname)
        path_found, data, content_type = path.find_path()
        if path_found:
            status = status_code.HTTP_201_OK if headers["HTTP_METHOD"] == "POST" else status_code.HTTP_200_OK
            response = Response(status_code=status, data=data, content_type=content_type, headers=headers)
            return response.render_response()

        response = Response(status_code=status_code.HTTP_404_NOT_FOUND, data="", content_type=content_type, headers=headers)
        return response.render_response()

    def parse_headers(self) -> Response:
        # Split the request into its different headers.
        request_header = self.get_request_header()
        user_agent_header = self.get_user_agent_header()
        accept_encoding_header = self.get_encoding_header()

        headers = {**request_header, **user_agent_header, **accept_encoding_header}
        return self.check_path(headers=headers)
