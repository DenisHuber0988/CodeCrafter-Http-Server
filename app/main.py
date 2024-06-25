import argparse
import logging
import threading

from app.connection import ConnectionHandler
from app.parser import Parser

logger = logging.getLogger("socket_server")


DIR_FLAG = "--directory"


def handle_connection(handler, connection):
    """
    Handle the connection, read the request, send the response and finally close the connection.

    :param handler: ConnectionHandler
    :param connection: Connection issued from the ConnectionHandler.
    :return:
    """
    request = handler.read_request(connection=connection)
    parser = Parser(request=request, dirname=args.directory)
    response = parser.parse_headers()
    # Send the appropriate response to the client.
    handler.send_response(connection=connection, response=response)
    # Closing the connection.
    handler.close_connection(connection=connection)


def main():
    # Create a server socket that listen on localhost at port 4221
    handler = ConnectionHandler(reuse_port=True)
    server_socket = handler.create_server()

    while True:
        connection, _ = handler.accept_connection(server_socket=server_socket)
        # Read the request.
        thread = threading.Thread(target=handle_connection, args=(handler, connection))
        thread.start()


if __name__ == "__main__":
    # Parse the input.
    parse = argparse.ArgumentParser()
    parse.add_argument("--directory", required=False)
    args = parse.parse_args()
    main()


"""
import argparse
import os
import socket

from threading import Thread

# Data read
BUFF_SIZE = 1024
# Status code
HTTP_200_OK = "HTTP/1.1 200 OK"
HTTP_404_NOT_FOUND = "HTTP/1.1 404 Not Found"

# Content-Type
TEXT_PLAIN = "Content-Type: text/plain"
OCTET_STREAM = "Content-Type: application/octet-stream"

class Connection(Thread):

    def __init__(self, server_socket, address):
        super().__init__()
        self.sock = server_socket
        self.addr = address
        self.start()

    def run(self):
        print(f"Started thread with {self.addr}")
        resp = self.req().decode().splitlines()
        _, path, _ = resp[0].split(" ")
        parsed_headers = dict(line.split(": ", 1) for line in resp[1:-2])
        if path == "/":
            self.resp([HTTP_200_OK, "", ""])
        elif path.startswith("/echo/"):
            self.resp(
                [
                    HTTP_200_OK,
                    TEXT_PLAIN,
                    f"Content-Length: " + str(len(path[6:])),
                    "",
                    path[6:],
                ]
            )
        elif path == "/user-agent":
            self.resp(
                [
                    HTTP_200_OK,
                    TEXT_PLAIN,
                    f'Content-Length: {len(parsed_headers["User-Agent"])}',
                    "",
                    parsed_headers["User-Agent"],
                ]
            )
        elif path.startswith("/files/"):
            print(os.listdir(args.directory))
            print(os.path.join(args.directory, path[7:]))
            if os.path.exists(os.path.join(args.directory, path[7:])):
                with open(os.path.join(args.directory, path[7:]), "r") as f:
                    file_content = f.read()
                self.resp(
                    [
                        HTTP_200_OK,
                        OCTET_STREAM,
                        f"Content-Length: {len(file_content)}",
                        "",
                        file_content,
                    ]
                )
            else:
                self.resp(
                    [
                        HTTP_404_NOT_FOUND,
                        TEXT_PLAIN,
                        f"Content-Length: 3",
                        "",
                        "404",
                    ]
                )
        else:
            self.resp(
                [
                    HTTP_404_NOT_FOUND,
                    TEXT_PLAIN,
                    f"Content-Length: 3",
                    "",
                    "404",
                ]
            )

    def req(self):
        return self.sock.recv(BUFF_SIZE)

    def resp(self, args: list):
        print("------------")
        print("\r\n".join(args))
        print("------------")
        self.sock.send("\r\n".join(args).encode())


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    while True:
        client, client_addr = server_socket.accept()  # wait for client
        Connection(client, client_addr)


if __name__ == "__main__":
    parse = argparse.ArgumentParser()
    parse.add_argument("--directory", required=False)
    args = parse.parse_args()
    main()

"""