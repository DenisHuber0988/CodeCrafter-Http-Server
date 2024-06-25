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

    def get_request_header(self):
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

    def check_path(self, headers):
        request_header, user_agent_header = headers
        _, requested_path, http_version = request_header.split()

        path = Path(requested_path=requested_path, headers=[user_agent_header], dirname=self.dirname)
        path_found, data = path.find_path()
        if path_found:
            response = Response(http_version=http_version, status_code=status_code.HTTP_200_OK, data=data)
            return response.render_response()

        response = Response(http_version=http_version, status_code=status_code.HTTP_404_NOT_FOUND, data="")
        return response.render_response()

    def parse_headers(self) -> Response:
        # Split the request into its different headers.
        request_header = self.get_request_header()
        user_agent_header, _ = self.get_user_agent_and_accept_headers()
        return self.check_path(headers=[request_header, user_agent_header])
