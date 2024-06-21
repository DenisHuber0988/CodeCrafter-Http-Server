import logging
import socket


logger = logging.getLogger("socket_server")


SERVER_HOST = "localhost"
SERVER_PORT = 4221

OK_RESPONSE = b"HTTP/1.1 200 OK\r\n\r\n"

def main():

    # Create a server socket that listen on localhost at port 4221
    server_socket = socket.create_server((SERVER_HOST, SERVER_PORT), reuse_port=True)

    while True:
        # Wait for an incoming connection.
        logger.info(f"Connecting to {SERVER_HOST} on port {SERVER_PORT}")
        connection, _ = server_socket.accept()
        logger.info("Sending ok response to client.")
        connection.sendall(OK_RESPONSE)


if __name__ == "__main__":
    main()
