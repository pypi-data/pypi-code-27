#!/usr/bin/env python
# -*- coding: utf-8 -*-
import six
import sys
import uuid

import tornado.ioloop
import tornado.web
import tornado.websocket
from tornado.websocket import WebSocketClosedError
from tornado.options import define, options, parse_command_line
from tornado import ioloop, gen
from tornado.ioloop import PeriodicCallback
import tornado.options
from tornado.queues import Queue
from tornado.locks import Lock
import logging
import tornadoredis
from owcp.redisConnection import get_redis_connection
from validator import validate, Required, Pattern, In, Range

import json
import requests
import django

from django.conf import settings

django.setup()
try:
    from urlparse import urlparse # Py 2
except ImportError:
    from urllib.parse import urlparse # Py 3

from datetime import datetime
import time
from django.utils.timezone import now

try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse


# LOG = logging.getLogger("tornado.general")
LOG = logging.getLogger(__name__)
tornado.options.define("access_to_stdout", default=False, help="Log tornado.access to stdout")

# store clients in dictionary..
clients = dict()

STATUS_ABNORMAL_CLOSED = 1001
AUTHENTICATION_FAILED = 4001
PARAMETER_MISSING = 4002
# 如果修改，需要同时修改
PING_INTERVAL = 5*1000
PING_TIMEOUT = 5*1000
MSG_INTERVAL = 2*1000


if settings.TAG == 'DEV' or settings.TAG == 'PROD':
    DJANGO_URL = 'https://' + settings.DOMAIN + '/api-token-verify/'
else:
    DJANGO_URL = 'http://' + settings.DOMAIN + '/api-token-verify/'
if settings.TAG == 'DEV' or settings.TAG == 'PROD':
    NOTIFICATION_URL = "https://" + settings.DOMAIN + "/owcp/send_notification/"
else:
    NOTIFICATION_URL = "http://" + settings.DOMAIN + "/owcp/send_notification/"

define('port', 8888, type=int, help='Server port')
define('allowed_hosts', default=settings.DOMAIN + ':443', multiple=True, help='Allowed hosts for cross domain connections')


# pool = tornadoredis.ConnectionPool(max_connections=10, wait_for_available=True)
pool = None


class WebSocketHandler(tornado.websocket.WebSocketHandler):
    # 消息队列和消息锁
    def __init__(self, *args, **kwargs):
        self.msg_queue = Queue(maxsize=100)
        self.msg_lock = Lock()

        self.msg_lock_2 = Lock()
        self.msg_queue_2 = list()
        self.msg_count = 0
        self.msg_ping_time = 0.5

        self.client_id = None
        self._redis_client = None
        self.heartbeat = None
        self.last_ping = 0
        self.last_pong = 0
        self.client_address = None
        self.allow_origin = options.allowed_hosts
        self.r = get_redis_connection()
        self.sid = None
        self.AUTH = False


        super(WebSocketHandler, self).__init__(*args, **kwargs)

        self.client_id = self.get_argument("id")
        try:
            if self.r.llen("user:{0}:pipe".format(self.client_id)) > 0:
                message = self.r.lindex("user:{0}:pipe".format(self.client_id), 0)
                msg = json.loads(message.encode("utf-8"))
                if 'seq' in msg:
                    count = int(msg['seq']) - 1
                else:
                    LOG.error('user {0} msg seq is not exist'.format(self.client_id))
                    message = self.r.lpop("user:{0}:pipe".format(self.client_id))
                    LOG.error('user {0} msg_not_seq is {1}'.format(self.client_id, message))
            else:
                count = self.r.get("user:{0}:msg_send_cnt".format(self.client_id))
                if count is None:
                    self.r.set("user:{0}:msg_send_cnt".format(self.client_id), 0)
                    count = 0
            self.add_header("Msg_Count", count)
            LOG.info("user {0} start msg_count is {1}".format(self.client_id, count))
        except WebSocketClosedError as e:
            LOG.error("user {0} msg_count error {1}".format(self.client_id, e.message))

        LOG.info("user {0} _init_".format(self.client_id))
        if self.client_id is None or self.get_argument("token") is None:
            LOG.error("user {0} input parameter missing!!!".format(self.client_id))
            self.close(code=PARAMETER_MISSING, reason="input parameter missing!")
        self.sid = "user:" + self.client_id + ":channel"
        # LOG.info('trying to do authentication')
        # self.do_authentication(self.get_argument("token").strip('\"'))
        # remote authentication
        headers = {'content-type': 'application/json'}
        token = self.get_argument("token").strip('\"')
        # LOG.info(token)
        payload = {"token": token}
        j = json.dumps(payload)
        response = requests.post(DJANGO_URL, data=j, headers=headers)
        LOG.info("user {0} authentication status {1}: {2}".format(self.client_id, response.status_code, response.content))
        if response.status_code == 200:
            self.AUTH = True
        else:
            LOG.error('user {0} authentication failed!'.format(self.client_id))

    @tornado.gen.coroutine
    def open(self, *args):
        # LOG.info("user {0} status code is {0}".format(status_code))
        if self.AUTH:
            LOG.info('user {0} authenticate success!'.format(self.client_id))
            if self.client_id in clients:
                yield tornado.gen.sleep(10)
            # self.close()
            # self._connect_to_redis()
            self._listen(self.sid)
            # ready for open
            LOG.info("user {0} open client id {0} self is {1}".format(self.client_id, self))
            self.stream.set_nodelay(True)

            clients[self.client_id] = self
            self.client_address = self.request.remote_ip
            LOG.info("user {0} remote address {1}".format(self.client_id, self.client_address))
            """
            :go fetch "user:id" from Redis
            """
            # 发送redis中的消息
            # self._send_msg()
            self.send_online_msg()

            sid = "user:" + self.client_id
            self.r.set(sid + ":online", "True")
            LOG.info(sid + ":online")

            self.last_ping = ioloop.IOLoop.current().time()
            self.last_pong = self.last_ping
            self.heartbeat = PeriodicCallback(self._send_ping, PING_INTERVAL,
                                              io_loop=ioloop.IOLoop.current())
            self.heartbeat.start()

            self.heartbeat_Msg = PeriodicCallback(self._send_msg, MSG_INTERVAL,
                                                  io_loop=ioloop.IOLoop.current())
            self.heartbeat_Msg.start()
        else:
            LOG.info('user {0}: authenticate failed!'.format(self.client_id))
            # LOG.error(r.text)
            self.close(code=AUTHENTICATION_FAILED, reason='Authentication Failed!')

    #@tornado.gen.coroutine
    def send_online_msg(self):
        sid = "user:" + self.client_id
        msg_list = self.r.lrange(sid + ":pipe", 0, -1)
        for message in msg_list:
            msg = json.loads(message.encode("utf-8"))
            LOG.info("user {0} : pipe online message is {1}".format(self.client_id, msg))
            self.write_message(msg)

    def _send_msg(self):
        # 每隔3s检查是否有消息，如果有新消息，则一条一条发送，发送后，如果在on_message中接收到回复，则在on_message中发送下一条消息
        sid = "user:" + self.client_id
        if self.r.llen(sid + ":pipe") > 0:
            message = self.r.lindex(sid + ":pipe", 0)
            msg = json.loads(message.encode("utf-8"))
            LOG.info("user {0} : pipe online message is {1}".format(self.client_id, msg))
            self.write_message(msg)

    def incr_msg_send(self, user_id):
        return self.r.incr("{0}:msg_send_cnt".format(user_id))

    @tornado.gen.coroutine
    def _send_ping(self):
        LOG.info("user {0} enter heartbeat".format(self.client_id))
        if self.stream.closed() and self.heartbeat is None:
            LOG.info("user {0} self.stream.closed() and self.heartbeat is None".format(self.client_id))
            self.heartbeat.stop()
            self.force_close()
            return

        now = ioloop.IOLoop.current().time()
        since_last_pong = 1e3 * (now - self.last_pong)
        since_last_ping = 1e3 * (now - self.last_ping)

        if since_last_pong > 2 * PING_TIMEOUT:
            LOG.error("user {0} WebSocket ping timeout after %i ms.".format(self.client_id), since_last_pong)
            self.force_close()
            return
        try:
            # LOG.info('ready to ping')
            self.ping(str(datetime.now()))
            # LOG.info("user {0} send ping periodically")
            self.last_ping = now
            # print self.last_ping
        except WebSocketClosedError as e:
            LOG.error('user {0} WebSocketClosedError {1}'.format(self.client_id, e.message))
            self.force_close()
        except AttributeError as e:
            LOG.error('user {0} AttributeError {1}'.format(self.client_id, e.message))
            self.force_close()

    @tornado.gen.coroutine
    def force_close(self):
        # LOG.error("1. start force_close")
        self.r.set("user:" + self.client_id + ":online", "False")
        if self.heartbeat_Msg:
            self.heartbeat_Msg.stop()
            del self.heartbeat_Msg

        if self.heartbeat:
            self.heartbeat.stop()
            del self.heartbeat
            # LOG.error('2. delete heartbeat')
            #self.on_close()
            self.close(code=STATUS_ABNORMAL_CLOSED, reason="ping timeout")
        else:
            #self.on_close()
            self.close()
            pass
        self.r.connection_pool.disconnect()
        # LOG.error('end force_close')

    @tornado.gen.coroutine
    def on_message(self, message):
        """
        :param message (str, not-parsed JSON): data from client (web browser)
        """
        encoded_message = message.encode('utf8')
        LOG.info("user {1} on_message: {0}".format(encoded_message, self.client_id))
        try:
            msg = json.loads(encoded_message)
            if 'type' in msg and msg['type'] == 'reply':
                if self.r.llen("user:{0}:pipe".format(self.client_id)) > 0:
                    tmp_message = self.r.lindex("user:{0}:pipe".format(self.client_id), 0)
                    tmp_msg = json.loads(tmp_message.encode("utf-8"))
                    if msg['seq'] == tmp_msg['seq']:
                        tmp_message = self.r.lpop("user:{0}:pipe".format(self.client_id))
                        tmp_msg = json.loads(tmp_message.encode("utf-8"))
                        LOG.info("user {0} : pop msg {1}, payload is {2}".format(self.client_id, tmp_msg['seq'],
                                                                                 tmp_msg['msg']['payload']))
                # 收到消息回复，发送下一条消息
                self._send_msg()
                return
        except AttributeError as e:
            LOG.error('user {0} AttributeError {1}'.format(self.client_id, e.message))
            self.force_close()

        if self.is_ws_msg_valid(self.client_id, encoded_message):
            self.cons_ws_payload(encoded_message, self.client_id)

    def on_ping(self, data):
        LOG.info("user {0} on ping".format(self.client_id))

    def on_pong(self, data):
        self.last_pong = ioloop.IOLoop.current().time()
        # LOG.info("user {0} on pong {0}".format(data))

    @tornado.gen.coroutine
    def _on_update(self, message):
        """
        Receive Message from Redis when data become published and send it to selected client.
        :param message (Redis Message): data from redis

        need try catch
        """
        LOG.info('user {0} ### message.body {1}'.format(self.client_id, message))
        if isinstance(message.body, six.string_types):
            LOG.info('user {0} message obj is a string!'.format(self.client_id))
            try:
                body = json.loads(message.body)
            except ValueError as e:
                LOG.error("user {0} Exception {1}".format(self.client_id, e))
                LOG.error("user {0} Exception {1}".format(self.client_id, message.body))
                LOG.error("user {0} Exception {1}".format(self.client_id, message))
            try:
                if body:
                    #  消息计数加一，用于统计是否是关闭连接前的最后一条消息

                    self._send_msg()

            except(WebSocketClosedError, AttributeError):
                LOG.info('user {0} WebSocketClosedError when on_update'.format(self.client_id))
                self.force_close()

        # self.write_message(message.body)
        # if self.client_id == body['client_id']:
        #     print("entered!")
        #     self.write_message(message.body)

    @tornado.web.asynchronous
    @tornado.gen.engine
    def _listen(self, sid):
        """
        Listening chanel 'user:id'
        """
        for name, config in settings.STREAM_REDIS_CONFIG.items():
            self._redis_client = tornadoredis.Client(host=config['host'],
                                                     port=config['port'],
                                                     password=config['password'],
                                                     connection_pool=pool)
        LOG.info("user {0} listening:{1}".format(self.client_id, sid))
        yield tornado.gen.Task(self._redis_client.subscribe, sid)
        self._redis_client.listen(self._on_update)

    @tornado.gen.coroutine
    def on_close(self):
        """
        When client will disconnect (close web browser) then shut down connection for selected client
        websocket关闭时，会延迟5s
        """
        # 检查一遍缓存队列中是否有消息
        # self.write_msg_to_offline()

        LOG.error('user {0} start on_close function'.format(self.client_id))
        sid = "user:" + self.client_id
        LOG.info("user {0}:offline, websocket closed".format(self.client_id))
        # self.r.set(sid + ":online", "False")

        if self._redis_client:
            LOG.error('user {0} starting disconnect redis'.format(self.client_id))
            # self._redis_client.unsubscribe(sid + ":channel")
            # self._redis_client.disconnect
            yield tornado.gen.Task(self._redis_client.unsubscribe, sid + ":channel")
            yield tornado.gen.Task(self._redis_client.disconnect)
            LOG.info('user {0} succeeded disconnect redis'.format(self.client_id))
        else:
            LOG.info('user {0} when on_close, self._redis_client is None'.format(self.client_id))
        # del clients[self.client_id]

        # 这里可能有竞争存在，旧的websocket没有完全关闭时，又有了新的websocket，此时用户状态应该为在线
        if self.client_id in clients:
            if clients[self.client_id] == self:
                del clients[self.client_id]
        LOG.error('user {0} end on_close function'.format(self.client_id))

    def check_origin(self, origin):
        """
        Check if incoming connection is in supported domain
        :param origin (str): Origin/Domain of connection
        """
        # import re
        # bool(re.match(r'^.*?\.mydomain\.com', origin))
        # allowed = super.check_origin(origin)
        if self.allow_origin == '*':
            return True

        host = self.request.headers.get("Host")
        if origin is None:
            origin = self.request.headers.get("Origin")

        # If no header is provided, assume we can't verify origin
        if origin is None:
            LOG.warning("user {0} Missing Origin header, rejecting WebSocket connection.".format(self.client_id))
            return False
        if host is None:
            LOG.warning("user {0} Missing Host header, rejecting WebSocket connection.".format(self.client_id))
            return False

        origin = origin.lower()
        origin_host = urlparse(origin).netloc

        # OK if origin matches host
        if origin_host == host:
            return True

        # Check CORS headers
        if self.allow_origin:
            allow = self.allow_origin == origin
        # elif self.allow_origin_pat:
        #     allow = bool(self.allow_origin_pat.match(origin))
        else:
            # No CORS headers deny the request
            allow = False
        if not allow:
            LOG.warning("user {0} Blocking Cross Origin WebSocket Attempt.  Origin: %s, Host: %s",
                        self.client_id, origin, host)
        return allow

    def _connect_to_redis(self):
        """
        Extracts connection parameters from settings variable 'REDIS_URL' and
        connects stored client to Redis server.
        """
        for name, config in settings.STREAM_REDIS_CONFIG.items():
            self._redis_client = tornadoredis.Client(host=config['host'],
                                                     port=config['port'],
                                                     password=config['password'],
                                                     connection_pool=pool)
            self._redis_client.connect()

    # @gen.coroutine, if use coroutine, return can't recognize true or false.
    def is_ws_msg_valid(self, from_user_id, data):
        obj = json.loads(data)
        if 'type' not in obj:
            LOG.error("user {0} ###is_ws_msg_valid### type is not existed".format(self.client_id))
            return False
        rules = {
            "target": [Required, Pattern('[\S]{1,300}')],
            "payload": [Required, Pattern('[\s]{0,}[\S]{1,}')],
            "type": [In(["txt", "audio", "img"])]
        }
        if obj['type'] == 'img':
            rules.update({
                "width": [Range(1, 10000)],
                "height": [Range(1, 10000)],
            })
        validate_result = validate(rules, obj)
        if not validate_result.valid:
            LOG.error("user {0} ###is_ws_msg_valid #### msg format is not valid, {1}".format(self.client_id, obj))
            return False

        if obj['target']:
            try:
                t = obj['target'].split(':')
                if t[0] == 'user':
                    # check target user is friend
                    user_key = "{0}:friendlist".format(from_user_id)
                    f = self.r.zscan(user_key, 0, t[1], 1)
                    if not f and len(f[1]) == 0:
                        LOG.error("user {0} ###is_ws_msg_valid###sender and receiver is not friend.".format(
                            self.client_id))
                        return False
                elif t[0] == 'room':
                    # check is member of group
                    room_key = "room:{0}".format(t[1])
                    f = self.r.sscan_iter(room_key, from_user_id, 1)
                    if not f and len(f[1]) == 0:
                        LOG.error("user {0} ###is_ws_msg_valid###sender is not member of group".format(self.client_id))
                        return False
                else:
                    LOG.error("user {0} ###is_ws_msg_valid### target is not correct".format(self.client_id))
                    return False
            except ValueError:
                LOG.error("user {0} ###is_ws_msg_valid### target content error".format(self.client_id))
                return False
        else:
            LOG.error("user {0} ###is_ws_msg_valid### target is not exist".format(self.client_id))
            return False

        return True

    @tornado.gen.coroutine
    def cons_ws_payload(self, data, from_user_id):
        obj = json.loads(data)
        target_key = str(obj['target'])
        LOG.info("user {0} cons_ws_payload: target is {1}".format(self.client_id, target_key))

        user_json = self.r.hget("user:{0}:map".format(from_user_id), "profile")
        user_profile = None
        if user_json:
            user_profile = json.loads(user_json)
        else:
            LOG.error('user {0} ###cons_ws_payload### user profile is not existed'.format(self.client_id))
        try:
            # add new function
            if obj['type'] == 'img' or obj['type'] == 'audio':
                obj['payload'] = settings.OSS_IMG_DOMAIN + '/' + obj['payload']
            if target_key.split(':')[0] == 'user':
                payload = {
                    "msg_type": 'msg',
                    "msg": {
                        "type": obj['type'],
                        "payload": obj['payload'],
                        "id": str(uuid.uuid1()),
                        # datetime.datetime.utcnow().replace(tzinfo=pytz.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
                        "timestamp": now().strftime(settings.REST_FRAMEWORK['DATETIME_FORMAT'])
                    },
                    "from": user_profile,
                    "seq": self.incr_msg_send(target_key)
                }
                if obj['type'] == 'img':
                    payload['msg'].update(
                        {
                            "width": obj['width'],
                            "height": obj['height']
                        }
                    )
                json_content = json.dumps(payload, sort_keys=True, ensure_ascii=False).encode('utf8')
                LOG.info("user {0} cons_ws_payload: json_content {1}".format(self.client_id, json_content))

                if self.r.get(target_key + ":online") == "True":
                    LOG.info("user {0} {1} is online".format(self.client_id, target_key))
                    self.r.rpush(target_key + ":pipe", json_content)
                    self.r.publish(target_key + ":channel", json_content)
                else:
                    LOG.info("user {0} cons_ws_payload:{1} is offline".format(self.client_id, target_key))
                    # 发送离线通知
                    self.send_outside_app_notification([target_key], '您有一条新信息', payload)
                    self.r.rpush(target_key + ":pipe", json_content)
            elif target_key.split(':')[0] == 'room':
                room, room_id = target_key.split(':')
                LOG.info("user {0} cons_ws_payload:roomid is {1}, target {2}".format(self.client_id, room_id, target_key))
                m_nickname = self.r.hget("user:{0}:map".format(from_user_id), target_key)
                # redis encode still have some problem, don't directly print this log
                # LOG.info("user {0} cons_ws_payload: m_nickname is {0}".format(m_nickname.encode('utf-8')))
                if m_nickname and user_profile and 'name' in user_profile:
                    user_profile['name'] = m_nickname
                payload = {
                    "msg_type": 'room_msg',
                    "msg": {
                        "type": obj['type'],
                        "payload": obj['payload'],
                        "id": str(uuid.uuid1()),
                        "timestamp": now().strftime(settings.REST_FRAMEWORK['DATETIME_FORMAT'])
                    },
                    "room": room_id,
                    "from": user_profile
                }
                if obj['type'] == 'img':
                    payload['msg'].update(
                        {
                            "width": obj['width'],
                            "height": obj['height']
                        }
                    )
                json_content = json.dumps(payload, sort_keys=True, ensure_ascii=False).encode('utf8')
                # check if is room channel, publish to channel and check who is not online and set data to user:1:pipe
                # TODO and add APNS send
                room_user_list = self.r.smembers("room:{0}".format(room_id))
                if room_user_list:
                    room_user_list.remove(from_user_id)
                    offline_member_list = list()
                    for room_user_id in room_user_list:

                        payload['seq'] = self.incr_msg_send("user:{0}".format(room_user_id))
                        json_content = json.dumps(payload, sort_keys=True, ensure_ascii=False).encode('utf8')

                        if self.r.get("user:{0}:online".format(room_user_id)) == "True":
                            self.r.rpush("user:{0}:pipe".format(room_user_id), json_content)
                            self.r.publish("user:{0}:channel".format(room_user_id), json_content)
                        else:
                            self.r.rpush("user:{0}:pipe".format(room_user_id), json_content)
                            offline_member_list.append("user:"+str(room_user_id))
                            LOG.info(
                                "user {0} cons_ws_payload:add json to user:{1}:pipe due to user is offline".format(
                                    self.client_id, room_user_id))
                    # 发送离线通知
                    if len(offline_member_list) > 0:
                        self.send_outside_app_notification(offline_member_list, '您有一条新信息', payload)
                # this place need to optimize, because this is a synchronization. So maybe we can use async to finish it
        except ValueError:
            LOG.error("user {0} cons_ws_payload: construct WebSocket json payload error!!!".format(self.client_id))

    def send_outside_app_notification(self, target_list, msg, payload):
        """
        :param target_list: 格式为 ['user:144', 'user:34'...]
        :param msg:
        :param payload:
        """
        LOG.info("user {0} send_outside_app_notification:target_list is: {1}".format(self.client_id, target_list))
        headers = {'content-type': 'application/json'}
        token = self.get_argument("token").strip('\"')
        headers["Authorization"] = 'JWT {0}'.format(token)
        request_data = {'users': target_list, 'message': msg, 'payload': payload}
        response = requests.request(method='post', headers=headers,
                                    url=NOTIFICATION_URL,
                                    data=json.dumps(request_data))
        if response.status_code != 200:
            LOG.error("user {0} send_outside_app_notification:remote invoke send notification failed {1}:{2}".format(
                self.client_id, response.status_code, response.content))
        LOG.info("user {0} send_outside_app_notification: success! ".format(self.client_id))


def shutdown():
    ioloop = tornado.ioloop.IOLoop.instance()
    LOG.info('Stopping server.')

    def finalize():
        ioloop.stop()
        LOG.info('Stopped.')

    ioloop.add_timeout(time.time() + 1.5, finalize)


def bootstrap():
    tornado.options.parse_command_line(final=True)
    init_logging(tornado.options.options.access_to_stdout)


def init_logging(access_to_stdout=False):
    if access_to_stdout:
        access_log = logging.getLogger('tornado.access')
        access_log.propagate = False
        # make sure access log is enabled even if error level is WARNING|ERROR
        access_log.setLevel(logging.DEBUG)
        app_log = logging.getLogger("tornado.application")
        gen_log = logging.getLogger("tornado.general")
        stdout_handler = logging.StreamHandler(sys.stdout)
        access_log.addHandler(stdout_handler)
        app_log.addHandler(stdout_handler)
        gen_log.addHandler(stdout_handler)

