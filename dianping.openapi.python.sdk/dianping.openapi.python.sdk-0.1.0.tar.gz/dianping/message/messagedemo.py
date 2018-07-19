from wsclient import WebSocketClient
from tornado import ioloop



class RTCWebSocketClient(WebSocketClient):
    msg = {'msg_id': '1234'}

    def connecttest(self):
        io_loop = ioloop.IOLoop.instance()
        wsclient = RTCWebSocketClient('cecb5bd6ae79e7e1', 'acd63c7071198db36e91ffd316e7cf4ad990d350')
        wsclient.connect("ws://10.72.253.120:80/message/websocket")
        try:
            io_loop.start()
        except KeyboardInterrupt:
            wsclient.close()

    def closetest(self):
        wsclient = RTCWebSocketClient('cecb5bd6ae79e7e1', 'acd63c7071198db36e91ffd316e7cf4ad990d350')
        wsclient.connect("ws://10.72.251.238:80/message/websocket")
        wsclient.close(reason='')

    def reconnecttest(self):
        io_loop = ioloop.IOLoop.instance()
        wsclient = RTCWebSocketClient('cecb5bd6ae79e7e1', 'acd63c7071198db36e91ffd316e7cf4ad990d350')
        wsclient.reconnect(auto_reconnect=True)
        wsclient.on_message(self.msg)
        try:
            io_loop.start()
        except KeyboardInterrupt:
            wsclient.close()


if __name__ == '__main__':
    messagetest = RTCWebSocketClient('cecb5bd6ae79e7e1', 'acd63c7071198db36e91ffd316e7cf4ad990d350')
    messagetest.connecttest()
    messagetest.closetest()
    messagetest.reconnecttest()

