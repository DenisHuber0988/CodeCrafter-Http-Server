import logging
import socket

from app.paths import parse_path
from app import status_code

logger = logging.getLogger("socket_server")


# Data
BUFF_SIZE = 1024
CRLF = "\r\n"

# Server information
SERVER_HOST = "localhost"
SERVER_PORT = 4221

# Headers
CONTENT_TYPE_HEADER = "Content-Type: text/plain"
CONTENT_LENGTH_HEADER = "Content-Length: "
USER_AGENT_HEADER = "User-Agent: "
ACCEPT_HEADER = "Accept: "


def construct_response(http_version: str, status: list, data: str) -> bytes:
    # Construct the HTTP response based on the information received.
    code, reason = status
    base = f"{http_version} {code} {reason}"
    content_length = "".join([CONTENT_LENGTH_HEADER, str(len(data))])
    body = ""

    headers = [base, CONTENT_TYPE_HEADER, content_length, body, data]
    response = CRLF.join([header for header in headers])
    return response.encode()


def get_user_agent_and_accept(request) -> tuple[str, str]:
    # User_Agent_Header and Accept_Header appears and 2 and 3 place.
    # But for some reason (curl formatting ?), their places are sometime switched.
    user_agent_header, accept_header = request.split(CRLF)[2], request.split(CRLF)[3]

    if USER_AGENT_HEADER in user_agent_header:
        return user_agent_header, accept_header

    user_agent_header, accept_header = accept_header, user_agent_header  # Switching value.
    return user_agent_header, accept_header


def parse_buffer(request: str) -> bytes:
    # Split the request into its different headers.
    request_header = request.split(CRLF)[0]
    user_agent_header, _ = get_user_agent_and_accept(request=request)
    _, path, http_version = request_header.split()

    path_found, data = parse_path(path=path, headers=[user_agent_header])
    if path_found:
        return construct_response(http_version=http_version, status=status_code.HTTP_200_OK, data=data)

    return construct_response(http_version=http_version, status=status_code.HTTP_404_NOT_FOUND, data="")


def main():

    # Create a server socket that listen on localhost at port 4221
    server_socket = socket.create_server((SERVER_HOST, SERVER_PORT), reuse_port=True)

    while True:
        # Wait for an incoming connection.
        logger.info(f"Connecting to {SERVER_HOST} on port {SERVER_PORT}")
        connection, _ = server_socket.accept()
        request = connection.recv(BUFF_SIZE).decode("utf-8")
        print(f"{request =}")
        response = parse_buffer(request=request)
        logger.info("Sending ok response to client.")
        connection.sendto(response, (SERVER_HOST, SERVER_PORT))

        # Closing the connection
        connection.close()


if __name__ == "__main__":
    main()
