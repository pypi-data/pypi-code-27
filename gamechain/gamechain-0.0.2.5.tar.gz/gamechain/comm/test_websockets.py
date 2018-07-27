from socketIO_client import SocketIO, LoggingNamespace

SOCKETIO_SERVER = "https://test-bch-insight.bitpay.com"
SOCKETIO_SERVER = "https://bch-insight.bitpay.com"

def on_connect():
    print('connect')
    socketIO.emit('subscribe', "inv");

def on_disconnect():
    print('disconnect')

def on_reconnect():
    print('reconnect')

def on_aaa_response(*args):
    print('on_aaa_response', args)

def on_tx(data):
    print(f"TX: {data}")


socketIO = SocketIO(SOCKETIO_SERVER, namespace=LoggingNamespace)
socketIO.on('connect', on_connect)
socketIO.on('disconnect', on_disconnect)
socketIO.on('reconnect', on_reconnect)

socketIO.on("tx", on_tx)

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
socketIO.wait(seconds=100)