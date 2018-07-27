import threading
from socketIO_client import SocketIO, LoggingNamespace

SOCKETIO_SERVER = "https://test-bch-insight.bitpay.com"
# SOCKETIO_SERVER = "https://bch-insight.bitpay.com"


class GameChainMonitor:

    def __init__(self, wait_time=60):
        self._tx_handler = None
        monitor_thread = threading.Thread(target=self._start_monitor)
        monitor_thread.start()

    def _start_monitor(self):
        self._socketIO = SocketIO(SOCKETIO_SERVER, namespace=LoggingNamespace)
        self._socketIO.on('connect', self.on_connect)
        self._socketIO.on('disconnect', self.on_disconnect)
        self._socketIO.on('reconnect', self.on_reconnect)
        self._socketIO.on("tx", self.on_tx)

        self._socketIO.wait()

    def on_connect(self):
        print('connect')
        self._socketIO.emit('subscribe', "inv");

    def on_disconnect(self):
        print('disconnect')

    def on_reconnect(self):
        print('reconnect')

    def on_aaa_response(*args):
        print('on_aaa_response', args)

    def on_tx(self, data):
        if self._tx_handler is not None:
            self._tx_handler(data)

    def register_tx_handler(self, tx_handler):
        self._tx_handler = tx_handler

    def un_register_tx_handler(self, tx_handler):
        if self._tx_handler is tx_handler:
            self._tx_handler = None
        else:
            raise Exception("Invalid tx handler")

    def stop(self):
        if hasattr(self, "_socketIO"):
            self._socketIO.disconnect()




    # socketIO = SocketIO(SOCKETIO_SERVER, namespace=LoggingNamespace)
    # socketIO.on('connect', on_connect)
    # socketIO.on('disconnect', on_disconnect)
    # socketIO.on('reconnect', on_reconnect)
    #
    # socketIO.on("tx", on_tx)

    # # Listen
    # socketIO.on('aaa_response', on_aaa_response)
    # socketIO.emit('aaa')
    # socketIO.emit('aaa')
    # socketIO.wait(seconds=1)
    #
    # # Stop listening
    # socketIO.off('aaa_response')
    # socketIO.emit('aaa')
    # socketIO.wait(seconds=1)
    #
    # # Listen only once
    # socketIO.once('aaa_response', on_aaa_response)
    # socketIO.emit('aaa')  # Activate aaa_response
    # socketIO.emit('aaa')  # Ignore
    # socketIO.wait(seconds=100)
