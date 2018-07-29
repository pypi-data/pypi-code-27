# server.py
import socket
from python_asip_client.boards.serial_board import SerialBoard
from time import sleep
import sys


class TCPHandler:

    def __init__(self, port=9999):
        # Create a socket object
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = "0.0.0.0"
        self.port = port
        self.chunk = 1024
        # Bind to the port
        self.serversocket.bind((self.host, self.port))
        self.clientsocket, self.client_address = None, None
        self.connected = False
        self._serial_writer = None
        self.start_connection()
        self.serial_board = None

    def add_serial_writer(self, serial_board_):
        """
        This function takes a serial board object and adding serial board and serial writer to this class variables.
        :param serial_board_:
        :return:
        """
        self.serial_board = serial_board_
        self._serial_writer = serial_board_.get_asip_client().get_asip_writer()

    def start_connection(self):
        """
        Establishes new tcp connection using specified parameters.
        :return:
        """
        sys.stdout.write("Server waiting for connection on: {} port: {}\n".format(self.host, self.port))
        # Queue up to 5 requests
        self.serversocket.listen(5)
        # Here is waiting for a connection
        self.clientsocket, self.client_address = self.serversocket.accept()
        self.clientsocket.setblocking(1)
        self.connected = True
        sys.stdout.write("Set up new connection with: {}\n".format(self.client_address))

    def receive_data(self):
        """
        This function is handling receiving data from tcp connection.
        :return:
        """
        if self.connected:
            try:
                # Receive no more than 1024 bytes
                response = self.clientsocket.recv(self.chunk)
                if response and response is not None:
                    response = response.decode()
                    self._serial_writer.write(response)

            except socket.error as error:
                self.connected = False
                sys.stdout.write("TCP error while receiving data: {}\n".format(error))
                self.serial_board.thread_killer()
                sleep(2)
                self.connected = False
            except KeyboardInterrupt:
                self.close_bridge()

    def close_bridge(self):
        """
        Close tcp connection and serial thread.
        :return:
        """
        self.clientsocket.close()
        self.serversocket.close()
        self.serial_board.thread_killer()
        sleep(2)
        sys.stdout.write("Closing connection\n")
        sys.exit()

    def send_data(self, message):
        """
        Encoding messages and sending over tcp connection
        :param message: str
        :return:
        """
        try:
            if self.connected:
                message_to_send = message.encode()
                self.clientsocket.sendall(message_to_send)

        except socket.error as error:
            sys.stdout.write("Error while sending a data. Error: {}\n".format(error))
            self.connected = False

        except KeyboardInterrupt:
            self.close_bridge()


def run_tcp_bridge():
    """
    This function is initializing bridge main functions. It is also creating serial
    object and passing tcp to its listener thread. Serial has can either pass messages to tcp or to serial.
    In case of tcp dropping connection with host, it can re-establish by itself.
    :return:
    """
    tcp_handler = TCPHandler()
    serial_board = SerialBoard(tcp_handler)
    tcp_handler.add_serial_writer(serial_board)
    while tcp_handler.connected:
        tcp_handler.receive_data()
    else:
        del tcp_handler
        del serial_board
        run_tcp_bridge()


if __name__ == '__main__':
    run_tcp_bridge()
