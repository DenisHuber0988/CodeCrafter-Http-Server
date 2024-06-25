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
