from app import status_code
from app.constant import CRLF
from app.paths import Path
from app.response import Response


class Parser:
    """
    Parse the incoming request from the Server, and return a constructed Response.
    """

    def __init__(self, request, dirname):
        """
        :param request: The request sent by the client.
        :param dirname: The directory name from where to read a file.
        """
        self.request = request
        self.dirname = dirname

    def get_request_header(self) -> str:
        return self.request.split(CRLF)[0]

    def get_user_agent_and_accept_headers(self) -> tuple[str, str] | tuple[None, None]:
        # User_Agent_Header and Accept_Header appears and 2 and 3 place.
        # But for some reason (curl formatting ?), their places are sometime switched.
        try:
            user_agent_header, accept_header = self.request.split(CRLF)[2], self.request.split(CRLF)[3]
        except IndexError:
            return None, None

        if Response.USER_AGENT_HEADER in user_agent_header:
            return user_agent_header, accept_header

        user_agent_header, accept_header = accept_header, user_agent_header  # Switching value.
        return user_agent_header, accept_header

    def fetch_data(self):
        return self.request.split(CRLF)[-1]

    def check_path(self, headers) -> Response:
        request_header, user_agent_header = headers
        method, requested_path, http_version = request_header.split()
        body = self.fetch_data() if method == "POST" else None

        path = Path(
            method=method,
            requested_path=requested_path,
            headers=[user_agent_header],
            dirname=self.dirname,
            body=body,
        )
        path_found, data = path.find_path()
        if path_found:
            status = status_code.HTTP_201_OK if method == "POST" else status_code.HTTP_200_OK
            response = Response(http_version=http_version, status_code=status, data=data)
            return response.render_response()

        response = Response(http_version=http_version, status_code=status_code.HTTP_404_NOT_FOUND, data="")
        return response.render_response()

    def parse_headers(self) -> Response:
        # Split the request into its different headers.
        request_header = self.get_request_header()
        user_agent_header, _ = self.get_user_agent_and_accept_headers()
        return self.check_path(headers=[request_header, user_agent_header])
