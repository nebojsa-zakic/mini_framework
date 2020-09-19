import mini_http.conn_handler as conn_handler
import socket
import threading
from datetime import datetime as dt
import mini_http.log.logger as log

port = 5000


def server_port(port_number):
    global port
    if log.is_debugging():
        log.debug("Server port has been configured to: " + str(port_number))
    port = port_number


def _server_loop(sock):
    log.trace("Server is awaiting new connections.")
    while True:
        connection, client_address = sock.accept()
        if log.is_tracing():
            log.trace("New request from: " + str(client_address[0]))

        conn_thread = threading.Thread(
            target=conn_handler.handle_conn, args=(connection,))
        conn_thread.start()


def start():
    global port

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    sock.bind(('localhost', port))

    sock.listen(1)

    _server_loop(sock)
