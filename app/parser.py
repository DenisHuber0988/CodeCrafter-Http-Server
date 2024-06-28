from app import status_code
from app.constant import CRLF
from app.paths import Path
from app.response import Response
from app.utils import remove_none_elements_from_list


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

    def get_request_header(self) -> str:
        """
        Parse the first part of the request with Method - Path - Http-Version.
        """
        return self.request.split(CRLF)[0]

    def get_user_agent_header(self) -> str | None:
        """
        Parse the User-Agent: header from the request.
        """
        for header in self.request.split(CRLF):
            if header.startswith(self.USER_AGENT_HEADER):
                return header

        return None

    def get_accept_header(self) -> str | None:
        """
        Parse the Accept: header from the request.
        """
        for header in self.request.split(CRLF):
            if header.startswith(self.ACCEPT_ENCODING):
                return header

        return None

    def fetch_data(self) -> str:
        """
        In a POST scenario, the data/body to process are found at the end of the request.
        """
        return self.request.split(CRLF)[-1]

    def get_encoding_header(self) -> str | None:
        """
        Parse the request and try to find the Accept-Encoding header
        """
        for header in self.request.split(CRLF):
            if header.startswith(Response.ACCEPT_ENCODING_HEADER):
                return header

        return None

    def check_path(self, request, headers) -> Response:
        user_agent_header = headers[0] if headers != [] else None

        method, requested_path, http_version = request.split()
        body = self.fetch_data() if method == "POST" else None

        path = Path(
            method=method,
            requested_path=requested_path,
            user_agent_header=user_agent_header,
            dirname=self.dirname,
            body=body,
        )
        path_found, data = path.find_path()
        if path_found:
            status = status_code.HTTP_201_OK if method == "POST" else status_code.HTTP_200_OK
            response = Response(http_version=http_version, status_code=status, data=data, headers=headers)
            return response.render_response()

        response = Response(
            http_version=http_version,
            status_code=status_code.HTTP_404_NOT_FOUND,
            data="",
            headers=headers
        )
        return response.render_response()

    def parse_headers(self) -> Response:
        # Split the request into its different headers.
        request_header = self.get_request_header()
        user_agent_header = self.get_user_agent_header()
        accept_encoding_header = self.get_encoding_header()

        headers = remove_none_elements_from_list([user_agent_header, accept_encoding_header])
        return self.check_path(request=request_header, headers=headers)
