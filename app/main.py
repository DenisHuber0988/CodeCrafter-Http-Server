import logging
import socket


logger = logging.getLogger("socket_server")


# Data
BUFF_SIZE = 1024

# Server information
SERVER_HOST = "localhost"
SERVER_PORT = 4221

# Response
OK_RESPONSE = b"HTTP/1.1 200 OK\r\n\r\n"
NOT_OK_RESPONSE = b"HTTP/1.1 404 OK\r\n\r\n"
CRLF = "\r\n"


def parse_headers(data: str):
    # Split the data into its different component (part 1).
    method, request_target, http_version, _, server, user_agent = data.split(" ")

    if request_target == "/":
        return OK_RESPONSE

    return NOT_OK_RESPONSE

def main():

    # Create a server socket that listen on localhost at port 4221
    server_socket = socket.create_server((SERVER_HOST, SERVER_PORT), reuse_port=True)

    while True:
        # Wait for an incoming connection.
        logger.info(f"Connecting to {SERVER_HOST} on port {SERVER_PORT}")
        connection, address = server_socket.accept()
        data = connection.recv(BUFF_SIZE)
        response = parse_headers(data=str(data))
        print(f"{data = }")
        logger.info("Sending ok response to client.")
        connection.sendto(response, (SERVER_HOST, SERVER_PORT))

        # Closing the connection
        connection.close()


if __name__ == "__main__":
    main()
