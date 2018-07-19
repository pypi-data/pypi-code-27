#coding=utf-8


class App():
    def __init__(self):
        pass

    def __init__(self, appKey, appSecret):
        self.appKey = appKey
        self.appSecret = appSecret

    def get_appKey(self):
        return self.appKey

    def get_appSecret(self):
        return self.appSecret

    def set_appKey(self, appKey):
        self.appKey = appKey

    def set_appSecret(self, appSecret):
        self.appSecret = appSecret



class ClientMessage():
    def __init__(self):
        pass

    def __init__(self, msgId, type, msg):
        self.msgId = msgId
        self.type = type
        self.msg = msg

    def get_msgId(self):
        return self.msgId

    def get_type(self):
        return self.type

    def get_msg(self):
        return self.msg

    def set_msgId(self, msgId):
        self.msgId = msgId

    def set_type(self, type):
        self.type = type

    def set_msg(self, msg):
        self.msg = msg

"""

 todo,App作为变量
"""

class ConnectConfig():
    def __init__(self):
        pass

    def __init__(self):
        self.wsAddress = None
        self.connectId = None
        self.app = None

    def get_wsAddress(self):
        return self.wsAddress

    def get_connectId(self):
        return self.connectId

    def get_app(self):
        return self.app

    def set_wsAddress(self, wsAddress):
        self.wsAddress = wsAddress

    def set_connectId(self, connectId):
        self.connectId = connectId

    def set_app(self, app):
        self.app = app




class HeartBeat():

    def __init__(self):
        pass

    def __init__(self, count, lastPing, lastPong):
        self.count = count
        self.lastPing = lastPing
        self.lastPong = lastPong

    def get_count(self):
        return self.count

    def get_lastPing(self):
        return self.lastPing

    def get_lastPong(self):
        return self.lastPong

    def set_count(self, count):
        self.count = count

    def set_lastPing(self, lastPing):
        self.lastPing = lastPing

    def set_lastPong(self, lastPong):
        self.lastPong = lastPong


class ServerMessage():
    def __init__(self, msg_id, app_key, type, msg, app_shop_id, open_shop_uuid, bid, version, retry, heartbeat, sign):
        self.msg_id = msg_id
        self.app_key = app_key
        self.type = type
        self.msg = msg
        self.app_shop_id = app_shop_id
        self.open_shop_uuid = open_shop_uuid
        self.bid = bid
        self.version = version
        self.retry = retry
        self.heartbeat = heartbeat
        self.sign = sign

    def __init__(self):
        pass

    def get_msg_id(self):
        return self.msg_id

    def get_app_key(self):
        return self.app_key

    def get_type(self):
        return self.type

    def get_msg(self):
        return self.msg

    def get_app_shop_id(self):
        return self.app_shop_id

    def get_open_shop_uuid(self):
        return self.open_shop_uuid

    def get_bid(self):
        return self.bid

    def get_version(self):
        return self.version

    def get_retry(self):
        return self.retry

    def get_heartbeat(self):
        return self.heartbeat

    def get_sign(self):
        return self.sign

    def set_msg_id(self, msg_id):
        self.msg_id = msg_id

    def set_app_key(self, app_key):
        self.app_key = app_key

    def set_type(self, type):
        self.type = type

    def set_msg(self, msg):
        self.msg = msg

    def set_app_shop_id(self, app_shop_id):
        self.app_shop_id = app_shop_id

    def set_open_shop_uuid(self, open_shop_uuid):
        self.open_shop_uuid = open_shop_uuid

    def set_bid(self, bid):
        self.bid = bid

    def set_version(self, version):
        self.version = version

    def set_retry(self, retry):
        self.retry = retry

    def set_heartbeat(self, heartbeat):
        self.heartbeat = heartbeat

    def set_sign(self, sign):
        self.sign = sign


class WsContext():
    def __init__(self):
        pass

    def __init__(self, messageHandler, heartBeat, wsClient):
        self.messageHandler = messageHandler
        self.heartBeat = heartBeat
        self.wsClient = wsClient


    def get_message_handler(self):
        return self.messageHandler

    def set_message_handler(self, messagehandler):
        self.messageHandler = messagehandler

    def get_hear_beat(self):
        return self.heartBeat

    def set_heart_beat(self, heartBeat):
        self.heartBeat = heartBeat

    def get_wsclent(self):
        return self.wsClient

    def set_wxclient(self, wsClient):
        self.wsClient = wsClient



