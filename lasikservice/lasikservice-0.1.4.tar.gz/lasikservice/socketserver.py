import socket
import threading
from os.path import basename

def debug(msg):
    # overwrite with your callback for debug messages
    pass

def onSubThreadCrash():
    # overwrite with your callback in order to gracefully shut down other threads
    pass

class SocketServer:
    def __init__(self, handler, host = "localhost", port = 1337, timeout = 1):
        self.connections = []
        self.shutdown = False
        t = threading.Thread(
                target = self._t_socketServer,
                args = (handler, host, port, timeout))
        t.start()

    def requestShutdown(self):
        self.shutdown = True

    def msgToAll(self, msg):
        for conn in self.connections:
            conn.send((msg + '\n').encode('ascii'))

    def _t_socketServer(self, handler, host, port, timeout):
        try: #TODO to big/general try/except
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                s.bind((host,port))
                s.settimeout(timeout)
                s.listen()

                debug("set up socket server listening on '{}:{}'".format(host,port))

                while not self.shutdown:
                    try:
                        conn, addr = s.accept()
                        debug("new socket connection from {}".format(addr))
                    except socket.timeout:
                        continue

                    t = threading.Thread(
                            target = self._t_socketConnListener,
                            args = (conn, handler, timeout))
                    self.connections.append(conn)
                    t.start()

                debug("closing socket listening on '{}:{}'".format(host,port))
        except Exception as e:
            onSubThreadCrash()
            raise e

    def _t_socketConnListener(self, conn, handler, timeout):
        try: #TODO to big a try
            conn.settimeout(timeout)

            remainder = ""
            while not self.shutdown:
                try:
                    data = conn.recv(1024)
                    if not data: # remote connection dropped
                        # remove self from open socket list
                        for n, c in enumerate(self.connections): #TODO make it a dict?
                            if conn == c:
                                break
                        self.connections.pop(n)
                        debug("socket connection with {} lost, {} connections remaining".format(
                            conn.getpeername(), len(self.connections)))
                        break
                except socket.timeout:
                    continue
                input_string = remainder + data.decode('ascii')
                head, sep, tail = input_string.partition('\n')
                while sep: # partition returns (input,'','') on failure
                    handler(head)
                    head, sep, tail = tail.partition('\n')
                # store the non \n-terminated bytes to append the next data to
                remainder = head

        except Exception as e:
            onSubThreadCrash()
            raise e

        debug("shutting down socket listener thread")

# ==================================================================================================

def main():
    """
    Example usage, starts a server on HOST:PORT and relays messages
    connected clients ==> server stdout
    connected clients <== server stdin
    """
    global debug

    import sys

    if len(sys.argv) != 3:
        print("usage example: '{} HOST PORT'".format(basename(sys.argv[0])), file = sys.stderr)
        exit(1)
    host, port = sys.argv[1], int(sys.argv[2])

    debug = lambda msg: print("-- {} --".format(msg), file = sys.stderr)
    handler = lambda msg: print("someone says '{}'".format(msg))

    ss = SocketServer(handler, host = host, port = port, timeout = 1)
    for line in sys.stdin:
        ss.msgToAll("master says '{}'".format(line.strip()))
    ss.requestShutdown()

if __name__ == "__main__":
    main()
