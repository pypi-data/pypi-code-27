# _*_ coding:utf-8 _*_

import json
import logging
import time
from tornado import httpclient
from tornado import httputil
from tornado import ioloop
from tornado.websocket import WebSocketClientConnection
from dianping.message import messageutil
from dianping.message.msgentity import App
from dianping.message.msgentity import ConnectConfig
from tornado import gen
from msgentity import ClientMessage
import random

APPLICATION_JSON = 'application/json'


class WebSocketClient(object):
    connectconfig = ConnectConfig()

    min_heartbeat_interval = 5

    heartbeat_interval = 10

    randomnum = random.randint(0, 100)

    hb_msg = ClientMessage(randomnum, 'common.topic.clientheartbeat', 'heart_beat_msg')

    maxSleepTime = 120 * 1000

    maxReconnectNum = 30

    def __init__(self, appKey, appSecret):
        self.app = App(appKey, appSecret)
        self.connectconfig.set_app(self.app)
        self.connectconfig.set_connectId(messageutil.create_client_id())
        self._io_loop = ioloop.IOLoop.instance()
        self.last_active_time = 0
        self._ws_connection = None
        self._connect_status = False
        self.auto_reconnect = False
        self.ws_conn = None
        self.pending_hb = None

    '''connect the server'''

    def connect(self, wsAddress):
        try:
            self.connectconfig.set_wsAddress(wsAddress)
            url_link = messageutil.build_handle_snake_param(self.connectconfig.app, wsAddress,
                                                            self.connectconfig.connectId)
            headers = httputil.HTTPHeaders({'Content-Type': APPLICATION_JSON})
            request = httpclient.HTTPRequest(url=url_link, headers=headers)
            self.ws_conn = WebSocketClientConnection(request)
            self.ws_conn.connect_future.add_done_callback(self._connect_callback)
        except BaseException, e:
            logging.error('dianping.ws.sdk bootstrap error', e)

    '''close the server'''

    def close(self, reason=''):
        if self._connect_status:
            self._ws_connection and self._ws_connection.close()
            self._ws_connection = None
            self.on_connection_close(reason)
            self._connect_status = False

    def reconnect(self, auto_reconnect=True):
        sleepTime = 0
        i = 1
        self.auto_reconnect = auto_reconnect
        while i <= self.maxReconnectNum:
            if self.connectconfig.wsAddress is not None:
                if self.auto_reconnect:
                    sleepTime = min(sleepTime + 10 * 1000, self.maxSleepTime)
                    self.connect(self.connectconfig.wsAddress)
                    if self._connect_status:
                        continue
                    i = i + 1

    def send_heart_beat(self):
        print "heart"
        if self.is_connected():
            now = time.time()
            if now > (self.last_active_time + self.min_heartbeat_interval):
                self.last_active_time = now
                self.send(self.hb_msg)
        else:
            self.reconnect(auto_reconnect=True)
        #self.pending_hb = self._io_loop.call_later()

    '''send message to server'''

    def send(self, data):
        if self._connect_status:
            dict_data = data.__dict__
            write_msg = json.dumps(dict_data)
            self._ws_connection.write_message(write_msg)
            self.last_active_time = time.time()

    def is_connected(self):
        return self._ws_connection is not None

    def on_message(self, msg):
        if msg is not None:
            servermessage = json.loads(msg)
            if servermessage['type'] == 'common.topic.clientheartbeat':
                self._connect_status == True
            else:
                handlerresult = self.client_on_message(servermessage)
                if handlerresult or handlerresult is not None:
                    clientmessage = ClientMessage(servermessage['msg_id'], servermessage['type'], "ack");
                    self.send(clientmessage)
                    print 'test' + msg
                self._read_messages
        else:
            self.reconnect(auto_reconnect=True)

    def client_on_message(self, servermessage):
        """
        This is called when new message is available from the server.
        :param str msg: server message.
        """
        print 'test_client_on_message' + str(servermessage)
        return True

    def on_connection_success(self):
        """This is called on successful connection ot the server.
        """
        # self._io_loop.call_later(1,self.send_heart_beat())
        self.send_heart_beat()

    def on_connection_close(self, reason):
        """This is called when server closed the connection.
        """
        pass

    def on_pong(self):
        pass

    def on_ping(self, data):
        pass

    def _connect_callback(self, future):
        if future.exception() is None:
            self._connect_status = True
            self._ws_connection = future.result()
            self.on_connection_success()
            self._read_messages()
        else:
            self.close(future.exception())

    @gen.coroutine
    def _read_messages(self):
        while True:
            msg = yield self._ws_connection.read_message()
            print msg
            if msg is None:
                break
            self.on_message(msg)





