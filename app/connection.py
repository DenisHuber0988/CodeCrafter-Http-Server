import logging
import socket

logger = logging.getLogger(__name__)


class ConnectionHandler:
    """
    Represent a connection to the server.
    """

    # Server information.
    SERVER_HOST = "localhost"
    SERVER_PORT = 4221
    # Data read.
    BUFF_SIZE = 1024

    def __init__(self, reuse_port=False):
        super().__init__()
        self.host = self.SERVER_HOST
        self.port = self.SERVER_PORT
        self.reuse_port = reuse_port

    def create_server(self) -> socket.SocketType:
        logger.info(f"Create a server socket that listen on {self.host} on port {self.port}")
        return socket.create_server((self.host, self.port), reuse_port=self.reuse_port)

    def read_request(self, connection) -> str:
        return connection.recv(self.BUFF_SIZE).decode("utf-8")

    def send_response(self, connection, response) -> None:
        logger.info(f"Sending response: ** {response} ** to the server {self.host}:{self.port}")
        connection.sendto(response, (self.host, self.port))

    @staticmethod
    def accept_connection(server_socket) -> tuple[socket.SocketType, str]:
        logger.info("Wait for an incoming connection.")
        server_socket.listen()
        return server_socket.accept()

    @staticmethod
    def close_connection(connection) -> None:
        connection.close()
