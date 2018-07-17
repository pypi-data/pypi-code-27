"""
    This module contains the MuranoClient class that can be used to
    quickly create an object that can use either HTTP or MQTT.
"""
# pylint: disable=W1202

import time
import threading
import math
import logging
import sys
import six
import murano_client.constants
from murano_client.http import MuranoHTTP
from murano_client.mqtt import MuranoMQTT
if six.PY2:
    import Queue as queue
    from urlparse import urlparse
elif six.PY3:
    import queue
    from urllib.parse import urlparse


LOG = logging.getLogger(name='MURANO_CLIENT.Client')

class StoppableThread(threading.Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    def __init__(self, **kwargs):
        super(StoppableThread, self).__init__(**kwargs)
        self.__stop_event = threading.Event()

    def stop(self):
        """ Raise the stop event."""
        self.__stop_event.set()

    def stopped(self):
        """ Check if the stop event is set."""
        return self.__stop_event.is_set()

class WatchQueue(queue.Queue):
    """
        In an effort to stop writing try-except-Empty all over the place
        for handling queue.get() calls, implimenting a queue that returns
        None if the queue is empty.
    """
    def __init__(self, **kwargs):
        LOG.debug("kwargs: {}".format(kwargs))
        queue.Queue.__init__(self)

    def safe_get(self, timeout=None):
        """
            This function will block forever unless timeout is overridden.
            Returns data from the queue or None if timeout is reached with
            no data.
        """
        try:
            return self.get(timeout=timeout)
        except queue.Empty:
            return None

class InboundPayload(object):
    def __init__(self, **kwargs):
        self.payload = None
        self.timestamp = None
        self.resource = None
        protocol = kwargs.get('outbound_protocol')
        if protocol == 'mqtt':
            self.payload = kwargs.get('message').payload
            self.timestamp = kwargs.get('message').topic.split('/')[2]
            self.resource = kwargs.get('message').topic.split('/')[1]
        elif protocol == 'https':
            self.payload = kwargs.get('message').split('=')[1]
            self.timestamp = time.time()
            self.resource = kwargs.get('message').split('=')[0]

    def __str__(self):
        return "{}:{}={}".format(self.resource, self.timestamp, self.payload)

class OutboundPayload(object):
    def __init__(self, **kwargs):
        self.payload = kwargs.get('payload')
        self.timestamp = kwargs.get('timestamp')

        if kwargs.get('outbound_protocol') == 'mqtt':
            self.resource = '$resource/{}'.format(kwargs.get('resource'))
        elif kwargs.get('outbound_protocol') == 'https':
            self.resource = kwargs.get('resource')

    def __str__(self):
        return "{}:{}={}".format(self.resource, self.timestamp, self.payload)


class HTTPWatchThread(StoppableThread):
    def __init__(self, **kwargs):
        _ = LOG.setLevel(getattr(logging, kwargs.get('debug'))) if kwargs.get('debug') else None
        LOG.debug("kwargs: {}".format(kwargs))
        super(HTTPWatchThread, self).__init__()
        self.setDaemon(True)
        self.watch = kwargs.get('watch_function')
        self.name = '-'.join([self.__class__.__name__, kwargs.get('resource')])
        self.resource = kwargs.get('resource')
        self.watch_timeout = kwargs.get('http_timeout')
        self.inbound_queue = kwargs.get('inbound_queue')

    def run(self):
        since = 0.0

        while not self.stopped():
            LOG.info("(re)starting watch of: {}".format(self.resource))

            if since == 0.0:
                response = self.watch(self.resource)
            else:
                response = self.watch(
                    self.resource,
                    self.watch_timeout,
                    modify_ts=since)
            now = time.time()
            tdiff = now - since
            # TODO: the readhandler needs to parse a human-readable last-modified header.
            # since = response.last_modified or math.ceil(now)
            since = math.ceil(now)
            LOG.info('{} watched for {}s, got: {}'.format(self.__class__.__name__, tdiff, response))
            if response.code in [304, 204]:
                LOG.info("No new watch data.")
                continue
            if response.success:
                self.inbound_queue.put(
                    InboundPayload(
                        message=response.body,
                        outbound_protocol='https'
                    )
                )
            else:
                LOG.warning("http watcher was not successful: {}".format(response))


class HTTPTellThread(StoppableThread):
    """
        needs an outbound_queue
        objects going into the outbound queue need
        to be instances of OutboundPayload
    """
    def __init__(self, **kwargs):
        _ = LOG.setLevel(getattr(logging, kwargs.get('debug'))) if kwargs.get('debug') else None
        LOG.debug("kwargs: {}".format(kwargs))
        super(HTTPTellThread, self).__init__()
        self.setDaemon(True)
        self.name = self.__class__.__name__
        self.tell = kwargs.get('tell_function')
        self.outbound_queue = kwargs.get('outbound_queue')

    def run(self):
        LOG.info("Starting tell thread.")
        while not self.stopped():
            tell = self.outbound_queue.safe_get(timeout=1.0)
            if tell:
                LOG.debug("Sending tell data: {}".format(tell))
                response = self.tell(
                    {tell.resource: {tell.timestamp: tell.payload}})
                LOG.info("Tell response: {}".format(response))
        LOG.critical("{} has stopped!".format(self))

class MQTTTellThread(StoppableThread):
    """
        needs an outbound_queue
        objects going into the outbound queue need
        to be instances of OutboundPayload
    """
    def __init__(self, **kwargs):
        _ = LOG.setLevel(getattr(logging, kwargs.get('debug'))) if kwargs.get('debug') else None
        LOG.debug("kwargs: {}".format(kwargs))
        super(MQTTTellThread, self).__init__()
        self.setDaemon(True)
        self.name = self.__class__.__name__
        self.tell = kwargs.get('tell_function')
        self.outbound_queue = kwargs.get('outbound_queue')

    def run(self):
        while not self.stopped():
            LOG.info("starting tell thread")
            tell = self.outbound_queue.safe_get(timeout=1.0)
            if tell and tell.resource:
                # TODO: when either or both of MUR-6791 and MUR-7122 are fixed, the commented
                # code, below can be utilized to do records. For now, 
                # payload = [{'timestamp': tell.timestamp, 'values': {tell.resource: tell.payload}}]
                # LOG.info("telling to resource {}: {}".format(tell.resource, payload))
                LOG.info("telling to resource {}: {}".format(tell.resource, tell.payload))
                # response = self.tell('$resource.batch', json.dumps(payload), qos=1)
                response = self.tell(
                    tell.resource,
                    # json.dumps(payload),
                    tell.payload,
                    qos=1)
                LOG.info(response)
            else:
                LOG.debug(
                    "No resource defined in outbound payload object. Cannot tell Murano anything.")
        LOG.critical("{} has stopped!".format(self))


class MQTTWatchThread(StoppableThread):
    def __init__(self, **kwargs):
        _ = LOG.setLevel(getattr(logging, kwargs.get('debug'))) if kwargs.get('debug') else None
        LOG.debug("kwargs: {}".format(kwargs))
        super(MQTTWatchThread, self).__init__()
        self.setDaemon(True)
        self.watch = kwargs.get('watch_function')
        self.name = '-'.join([self.__class__.__name__, kwargs.get('resource')])
        self.resource = kwargs.get('resource')
        self.watch_timeout = kwargs.get('http_timeout')
        self.inbound_queue = kwargs.get('inbound_queue')

    def run(self):
        since = 0.0
        while not self.stopped():
            LOG.info("starting watch of: {}".format(self.resource))

            message = self.watch(timeout=self.watch_timeout)
            now = time.time()
            tdiff = now - since
            since = math.ceil(now)
            LOG.info('watch time {}: {}'.format(tdiff, message))
            if message:
                LOG.info(
                    "putting new message in inbound queue!")
                self.inbound_queue.put(InboundPayload(message=message, outbound_protocol='mqtt'))
        LOG.critical("{} has stopped!".format(self))

class MuranoClientException(Exception):
    pass

class MuranoClient(MuranoHTTP, MuranoMQTT):
    def __init__(self, **kwargs):
        """
            The inbound queue is designed so that objects of this class can call
            inbound_queue.safe_get([timeout]) and the payload objects from Murano
            will be formatted in a predictable way.

                Payload format of items in inbound_queue:

                    <resource>=
        """
        LOG.debug("Initializing MuranoHTTP Client...")
        self.inbound_queue = WatchQueue() # data from murano
        self.outbound_queue = WatchQueue() # data to murano
        self.outbound_protocol = None

        murano_host = kwargs.get('murano_host', None)
        if murano_host:
            self.outbound_protocol = urlparse(murano_host).scheme

        LOG.info("Using protocol {}".format(self.outbound_protocol))

        if not self.outbound_protocol:
            if six.PY3:
                sys.tracebacklimit = None
            else:
                sys.tracebacklimit = 0
            raise MuranoClientException(
                "Cannot parse supported protocol from murano_host parameter: {}"
                .format(kwargs.get('murano_host')))

        if not kwargs.get('watchlist'):
            if six.PY3:
                sys.tracebacklimit = None
            else:
                sys.tracebacklimit = 0
            raise MuranoClientException(
                "Required parameter 'watchlist' empty or not provided: {}"
                .format(kwargs.get('watchlist')))

        if self.outbound_protocol == 'mqtt': # no need for this for http
            kwargs['queue_inbound_messages'] = WatchQueue()
            MuranoMQTT.__init__(self, **kwargs)
        elif self.outbound_protocol == 'https':
            MuranoHTTP.__init__(self, **kwargs)

        if not self.murano_host():
            raise MuranoClientException("no murano_host specified.")

        self.watch_threads = []

        # ###################################################### #
        # ########### HTTP HTTP HTTP HTTP HTTP ################# #
        # ###################################################### #

        if self.outbound_protocol == 'https':
            for resource in kwargs.get('watchlist'):
                LOG.info('watching: {}'.format(resource))
                self.watch_threads.append(
                    HTTPWatchThread(
                        watch_function=self.http_long_poll,
                        inbound_queue=self.inbound_queue,
                        resource=resource,
                        http_timeout=kwargs.get(
                            'http_timeout',
                            murano_client.constants.DEFAULT_HTTP_TIMEOUT)*1000
                    )
                )
            LOG.critical("done init'ing thread objects.")

            self.tell_thread = HTTPTellThread(
                outbound_queue=self.outbound_queue,
                tell_function=self.http_record)

        # ###################################################### #
        # ########### MQTT MQTT MQTT MQTT MQTT ################# #
        # ###################################################### #

        elif self.outbound_protocol == 'mqtt':
            for resource in kwargs.get('watchlist'):
                LOG.info('watching: {}'.format(resource))
                self.watch_threads.append(
                    MQTTWatchThread(
                        watch_function=kwargs['queue_inbound_messages'].safe_get,
                        inbound_queue=self.inbound_queue,
                        resource=resource,
                        http_timeout=kwargs.get('http_timeout')*1000 if kwargs.get('http_timeout') else 10*1000
                    )
                )
            LOG.info("done init'ing thread objects.")
            # self.start_watchers()
            # LOG.info(self.watch_threads)

            self.tell_thread = MQTTTellThread(
                outbound_queue=self.outbound_queue,
                tell_function=self.publish)

            # tell_thread.start()
            # LOG.info("tell thread started")
        self.monitor_thread = StoppableThread(
            name='Monitor',
            target=self._monitor_thread,
            args=())
        self.monitor_thread.setDaemon(True)

    def stop_all(self):

        LOG.critical("Stopping all threads!!!")
        self.tell_thread.stop()
        LOG.critical("Waiting for {} to stop...".format(self.tell_thread))
        self.tell_thread.join()
        for watcher in self.watch_threads:
            if not watcher.stopped():
                watcher.stop()
            LOG.critical("Waiting for {} to stop...".format(watcher))
            watcher.join(timeout=0.25)
        if self.outbound_protocol == 'https':
            LOG.critical("Closing HTTP connection!!!")
            self.close_session()

        self.monitor_thread.stop()
        LOG.critical("Waiting for {} to stop...".format(self.monitor_thread))
        self.monitor_thread.join()
        LOG.critical("All threads have stopped.")
        return

    def start_client(self):
        if self.outbound_protocol == 'mqtt':
            self.start()
            self.loop_start()
        self.start_watchers()
        self.tell_thread.start()
        self.monitor_thread.start()

    def _monitor_thread(self):
        while not self.monitor_thread.stopped():
            for thread in threading.enumerate():
                LOG.info("running thread: {}".format(thread))
            LOG.info("inbound_queue size: {}".format(self.inbound_queue.qsize()))
            LOG.info("outbound_queue size: {}".format(self.outbound_queue.qsize()))
            time.sleep(5)
        LOG.critical("{} has stopped!".format(self.monitor_thread))

    def start_watchers(self):
        LOG.info("Starting watchers.")
        for thread in self.watch_threads:
            LOG.debug("starting: {}".format(thread))
            thread.setDaemon(True)
            thread.start()

    def tell(self, **kwargs):
        o_p = OutboundPayload(
            resource=kwargs.get('resource'),
            timestamp=kwargs.get('timestamp'),
            payload=kwargs.get('payload'),
            outbound_protocol=self.outbound_protocol)
        LOG.info("telling to outbound queue: {}".format(o_p))
        self.outbound_queue.put(o_p)

    def watch(self, **kwargs):
        if kwargs.get('timeout'):
            from_murano = self.inbound_queue.safe_get(timeout=kwargs.get('timeout'))
            LOG.info("got from murano, putting in inbound queue: {}".format(from_murano))
            return from_murano
        else:
            while True:
                from_murano = self.inbound_queue.safe_get(timeout=1.0)
                if from_murano:
                    LOG.info("got from murano, putting in inbound queue: {}".format(from_murano))
                    return from_murano
                else:
                    LOG.debug("No data from murano: {}".format(from_murano))


    def client_activate(self):
        if self.outbound_protocol == 'mqtt':
            self.start()
            self.mqtt_activate()
        elif self.outbound_protocol == 'https':
            self.http_activate()
