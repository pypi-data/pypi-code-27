# pylint: disable=C0103,C0301,C0325,W1202

import os
import ssl
import logging
import time
import six
from paho.mqtt.client import Client as PahoSNIMqttClient
from murano_client import BaseMuranoClient, __version__
if six.PY2:
    from urlparse import urlparse
elif six.PY3:
    from urllib.parse import urlparse

PahoReturnCodes = {
    0: "success, connection accepted",
    1: "connection refused, bad protocol",
    2: "refused, client-id error",
    3: "refused, service unavailable",
    4: "refused, bad username or password",
    5: "refused, not authorized"
}

LOG = logging.getLogger(name='MURANO_CLIENT.MuranoMQTT')


class MqttMsg(object):
    """
        This class is a wrapper class for MQTT
        messages. It is likely that he paho client
        will be used basicaly forever, but in the
        event that the protocol library changes,
        wrapping the message object will help
        us change the underlying library without
        breaking changes propagating upstream.
    """
    def __init__(self, msg):
        self.dup = msg.dup
        self.info = msg.info
        self.mid = msg.mid
        self.payload = msg.payload
        self.qos = msg.qos
        self.retain = msg.retain
        self.state = msg.state
        self.timestamp = msg.timestamp
        self.topic = msg.topic

class MqttPublishHandler(object):
    """
        ['__class__', '__delattr__', '__doc__', '__format__', '__getattribute__', '__getitem__',
        '__hash__', '__init__', '__iter__', '__module__', '__new__', '__next__', '__reduce__',
        '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__slots__', '__str__',
        '__subclasshook__', '_condition', '_iterpos', '_published', '_set_as_published',
        'is_published', 'mid', 'next', 'rc', 'wait_for_publish']
    """
    def __init__(self, msg_info):
        self.rc = msg_info.rc
        self.mid = msg_info.mid
        self.is_published = msg_info.is_published
        self.wait_for_publish = msg_info.wait_for_publish
        self.next = msg_info.next

class MuranoMQTT(PahoSNIMqttClient, BaseMuranoClient, object):
    def __init__(self, **kwargs):
        """
        :param pid: Specify the Murano Product ID. This will set the Vendor and the Model member variables to the same.

        :type  vendor: string
        """
        BaseMuranoClient.__init__(self, **kwargs)
        PahoSNIMqttClient.__init__(self, client_id="")
        _ = LOG.setLevel(getattr(logging, kwargs.get('debug'))) if kwargs.get('debug') else None

        LOG.debug("kwargs: {}".format(kwargs))
        tls_set_args = {'cert_reqs': ssl.CERT_OPTIONAL}
        if self.murano_cacert():
            tls_set_args.update(ca_certs=self.murano_cacert())

        if self.using_tls():
            tls_set_args.update({
                'certfile': self.certfile(),
                'keyfile': self.pkeyfile(),
            })
        LOG.info("tls_set_args: {}".format(tls_set_args))
        self.tls_set(**tls_set_args)
        # TODO: this is unacceptable: https://github.com/eclipse/paho.mqtt.python#tls_insecure_set
        self.tls_insecure_set(kwargs.get('tls_insecure_set') or False)
        uuid, pw = self.murano_id() if kwargs.get("password") else "", self.murano_token()
        LOG.info("setting username/password: id: {}, token: {}"
                 .format(uuid, pw))
        self.username_pw_set(uuid, pw)
        if not kwargs.get('murano_port'):
            LOG.debug("no murano_port specified. default to 8883")
            self.set_murano_port(8883)
        else:
            LOG.debug("murano_port overridden in kwargs: {}".format(kwargs.get('murano_port')))
            self.set_murano_port(kwargs.get('murano_port'))
        LOG.debug("mqtt host: {}, port: {}".format(
            self.murano_host(), self.murano_port()))

        self.on_log = self.default_on_log
        self.on_connect = self.default_on_connect
        self.on_disconnect = self.default_on_disconnect
        self.on_message = self.default_on_message
        self.on_publish = self.default_on_publish

        self.time_connected = 0.0
        self._connected = False
        self.connected = lambda: self._connected
        self.duration_connected = lambda: time.time() - self.time_connected
        self.put_messages_in_this_queue = kwargs.get('queue_inbound_messages')

    def __str__(self):
        return 'id: {} host: {} port: {} auth: {}'.format(
            self.murano_id(), self.murano_host(), self.murano_port(), self.using_tls())

    def default_on_log(self, client, userdata, level, buf):
        """ Default mqtt logger."""
        LOG.log(level, "client: {} userdata: {} buf: {} mid: {}"
                .format(client, userdata, buf, buf[buf.find('(')+len('Mid: ')+1:buf.find(')')]))

    def default_on_message(self, client, userdata, msg):
        """ Default on_message function for tunable logging. """
        LOG.info("dup: {} info: {} mid: {} qos: {} retain: {} state: {} timestamp: {} topic: {}"
                 .format(msg.dup,
                         msg.info,
                         msg.mid,
                         msg.qos,
                         msg.retain,
                         msg.state,
                         msg.timestamp,
                         msg.topic))
        LOG.debug("client: {} userdata: {} payload: {}"
                  .format(str(client), userdata, msg.payload))
        if self.put_messages_in_this_queue:
            LOG.info("Putting message in user-defined queue: {}".format(msg))
            self.put_messages_in_this_queue.put(msg)

    def default_on_publish(self, client, userdata, result):
        """ Default on_publish method for logging. """
        LOG.info("client: {} userdata: {} result (mid): {}"
                 .format(client, userdata, result))

    def default_on_connect(self, client, userdata, flags, rc):
        """ Default on_connect method for tracking connection status and logging. """
        LOG.info("client: {} userdata: {} flags: {} rc: {} reason: {}"
                 .format(client, userdata, flags, rc, PahoReturnCodes[rc]))
        self.time_connected = time.time()
        self._connected = True

    def default_on_disconnect(self, client, userdata, rc):
        """ Default on_disconnect method for tracking connection status and logging. """
        LOG.debug("client: {} userdata: {} rc: {} reason: {}"
                  .format(client, userdata, rc, PahoReturnCodes[rc]))
        LOG.info("time connected: {}".format(time.time()-self.time_connected))
        self.time_connected = 0.0
        self._connected = False
        if rc != 0:
            LOG.warning("ExositeMQTT default disconnection handler: {}, {}"\
                        .format(rc, PahoReturnCodes[rc]))
            self.connect(urlparse(self.murano_host()).netloc, self.murano_port())

    def mqtt_activate(self):
        default_callbacks = (self.on_connect, self.on_message)
        def on_connect(self, userdata, flags, rc):
            self.default_on_connect(self, userdata, flags, rc)
            LOG.debug("ExositeMQTT activation connection handler connected")
            LOG.debug("publish_activate_message...")
            rc, mid = self.publish("$provision/" + self.murano_id(), "", qos=1)
            LOG.debug("rc: {}, mid: {}, reason: {}".format(rc, mid, PahoReturnCodes[rc]))

        def on_message(self, userdata, msg):
            LOG.debug("Activation succeeded!")
            self.set_murano_token(msg.payload.decode())
            LOG.info(self.murano_token())
            self.username_pw_set("", self.murano_token())

            LOG.debug("activate_on_message: {} :: {} :: {}"
                      .format(self, userdata, msg.payload))

        if not self.using_tls():
            LOG.debug("Using token or user/pw method of provisioning.")
            self.on_connect = on_connect
            self.on_message = on_message
        else:
            LOG.debug("Using TLS Client Cert for provisioning.")

        self.loop_start()
        while not self.is_activated():
            LOG.debug("Waiting for activation...")
            time.sleep(1.0)
        LOG.debug("Activated.")
        self.on_connect, self.on_message = default_callbacks

    def start(self):
        LOG.info("starting...")
        try:
            self.connect(urlparse(self.murano_host()).netloc, self.murano_port())
            while not self.connected():
                self.loop()
                time.sleep(0.25)
                LOG.debug(".")
        except ssl.SSLError as exc:
            LOG.error(dir(exc))
            LOG.error(exc.errno)
            LOG.error(exc.reason)
            LOG.error(exc.strerror)
        LOG.info("started.")
