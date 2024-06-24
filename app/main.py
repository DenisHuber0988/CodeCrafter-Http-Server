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

# Representation Header
CONTENT_TYPE = "Content-Type: text/plain"


def construct_response(http_version, status, data):
    # Construct the HTTP response based the information received.
    base = f"{http_version} {status} {CRLF}"
    content_length = len(data)
    representation_header = f"{CONTENT_TYPE}{CRLF}Content-Length: {content_length}{CRLF}"
    response = "".join([base, representation_header])
    return response.encode()


def parse_buffer(request: str):
    # Split the data into its different component (part 1).
    header = request.split(CRLF)[0]
    _, path, http_version = header.split()

    path_found, data = parse_path(path)
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
        response = parse_buffer(request=request)
        logger.info("Sending ok response to client.")
        connection.sendto(response, (SERVER_HOST, SERVER_PORT))

        # Closing the connection
        connection.close()


if __name__ == "__main__":
    main()
