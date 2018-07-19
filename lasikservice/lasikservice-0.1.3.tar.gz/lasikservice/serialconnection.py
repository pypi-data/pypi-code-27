import re
import serial
import fcntl
import threading

def debug(msg):
    # overwrite with your callback for debug messages
    pass

def onSubThreadCrash():
    # overwrite with your callback in order to gracefully shut down other threads
    pass

# ==================================================================================================

class Connection:
    def __init__(self, path, recvHandler, timeout = 1):
        self.path = path
        self.shutdown = False
        self.ser = self._connect(timeout)
        self.recvThread = threading.Thread(target = self._t_listen, args=(recvHandler,))
        self.recvThread.start()
        self.awaitLock = None
        self.awaitReqResp = None

    def getPath(self):
        return self.path

    def close(self):
        debug("closing serial connection listening on {}".format(self.path))
        self.shutdown = True

    def _connect(self, timeout):
        try:
            ser = serial.Serial(self.path, timeout = timeout)
            # prevent multiple processes talking to one serial device by getting
            # an exclusive flock on the device file
            fcntl.lockf(ser,fcntl.LOCK_EX | fcntl.LOCK_NB)
        except (serial.SerialException, IOError) as e:
            errorMsg = "failed to connect to {}".format(self.path)
            debug(errorMsg)
            raise ConnectionError(errorMsg) from e
        debug("connected to {}".format(self.path))
        return ser

    def send(self, command):
        if not self.shutdown:
            self.ser.write("{}\n".format(command.strip()).encode('ascii'))
        else:
            errorMsg = ("cannot send command after shutdown ('{}' on {})".format(command, self.path))
            debug(errorMsg)
            raise Exception(errorMsg)

    def awaitResponse(self, command, response_regex):
        if self.awaitLock and self.awaitLock.locked():
            raise Exception("cannot wait for more than one response on same serial device")
        self.awaitLock = threading.Lock()
        self.awaitReqResp = response_regex
        self.awaitLock.acquire() # signals listen thread to listen for it
        self.send(command)
        self.awaitLock.acquire() # blocks until listen thread released it
        self.awaitLock = None
        return self.awaitReqResp # listen thread wrote match to this var

    def _t_listen(self, recvHandler):
        while not self.shutdown:
            try:
                msg = self.ser.readline().decode('ascii').strip()
                if msg:
                    if self.awaitLock and self.awaitLock.locked():  # waiting for matching response
                        m = re.match(self.awaitReqResp, msg)
                        if m:
                            self.awaitReqResp = msg
                            self.awaitLock.release() # signal to waiting thread it has been done
                    recvHandler(msg)
            except BaseException as e:
                onSubThreadCrash()
                raise e
        debug("thread listening on {} shut down".format(self.path))
        debug("releasing flock on {}".format(self.path))
        fcntl.lockf(self.ser,fcntl.LOCK_UN)

# ==================================================================================================

def main():
    """
    Example usage, and a basic tool to send/receive line separated messages on a serial device
    """

    import sys

    if len(sys.argv) != 2:
        print("usage example: '{} /dev/ttyACM0'".format(sys.argv[0]))
        exit(1)
    path = sys.argv[1]

    debug = lambda msg: print("-- {} --".format(msg), file = sys.stderr)
    l = Connection(path, print)
    for line in sys.stdin:
        l.send(line)
    l.close()

if __name__ == "__main__":
    main()
