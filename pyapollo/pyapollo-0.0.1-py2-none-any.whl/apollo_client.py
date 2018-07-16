# -*- coding: utf-8 -*-

"""
apollo python client
使用说明: http://wiki.intra.yongqianbao.com/pages/viewpage.action?pageId=11928499
author: sunguangran@daixiaomi.com
"""

import json
import logging
import sys
import threading
import time

import requests

apollo_logger = logging.getLogger(__name__)


class ApolloClient(object):

    def __init__(self, app_id, cluster='default', config_server_url='http://localhost:8080', timeout=90, ip=None):
        self.config_server_url = config_server_url
        self.appId = app_id
        self.cluster = cluster
        self.timeout = timeout
        self.stopped = False
        self.ip = self.init_ip(ip)

        self._stopping = False
        self._cache = {}
        self._notification_map = {'application': -1}

    def init_ip(self, ip):
        if ip:
            return ip

        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(('8.8.8.8', 53))
            return s.getsockname()[0]
        finally:
            if s:
                s.close()

    def get_value(self, key, default_val=None, namespace='application', auto_fetch_on_cache_miss=False):
        if namespace not in self._notification_map:
            self._notification_map[namespace] = -1
            apollo_logger.info("Add namespace '%s' to local notification map", namespace)

        if namespace not in self._cache:
            self._cache[namespace] = {}
            apollo_logger.info("Add namespace '%s' to local cache", namespace)
            # This is a new namespace, need to do a blocking fetch to populate the local cache
            self._long_poll()

        if key in self._cache[namespace]:
            return self._cache[namespace][key]

        if auto_fetch_on_cache_miss:
            return self._cached_http_get(key, default_val, namespace)

        return default_val

    # Start the long polling loop. Two modes are provided:
    # 1: thread mode (default), create a worker thread to do the loop. Call self.stop() to quit the loop
    # 2: eventlet mode (recommended), no need to call the .stop() since it is async
    def start(self, use_eventlet=False, catch_signals=True):
        apollo_logger.info('Start successful, appid: {}, server: {}, cluster: {}'.format(self.appId, self.config_server_url, self.cluster))

        # First do a blocking long poll to populate the local cache, otherwise we may get racing problems
        if len(self._cache) == 0:
            self._long_poll()

        if use_eventlet:
            import eventlet
            eventlet.monkey_patch()
            eventlet.spawn(self._listener)
        else:
            if catch_signals:
                import signal
                signal.signal(signal.SIGINT, self._signal_handler)
                signal.signal(signal.SIGTERM, self._signal_handler)
                signal.signal(signal.SIGABRT, self._signal_handler)
            t = threading.Thread(target=self._listener)
            t.setDaemon(True)
            t.start()

        return self

    def stop(self):
        self._stopping = True
        apollo_logger.info("Stopping listener...")

    def _cached_http_get(self, key, default_val, namespace='application'):
        url = '{}/configfiles/json/{}/{}/{}?ip={}'.format(self.config_server_url, self.appId, self.cluster, namespace, self.ip)
        r = requests.get(url)
        if r.ok:
            data = r.json()
            self._cache[namespace] = data
            apollo_logger.info('Updated local cache for namespace %s', namespace)
        else:
            data = self._cache[namespace]

        if key in data:
            return data[key]
        else:
            return default_val

    def _uncached_http_get(self, namespace='application'):
        url = '{}/configs/{}/{}/{}?ip={}'.format(self.config_server_url, self.appId, self.cluster, namespace, self.ip)
        r = requests.get(url)
        if r.status_code == 200:
            data = r.json()
            self._cache[namespace] = data['configurations']
            apollo_logger.info('Updated local cache for namespace %s release key %s: %s',
                               namespace, data['releaseKey'],
                               repr(self._cache[namespace]))

    def _signal_handler(self, signal, frame):
        apollo_logger.info('You pressed Ctrl+C!')
        self._stopping = True

    def _long_poll(self):
        url = '{}/notifications/v2'.format(self.config_server_url)
        notifications = []
        for key in self._notification_map:
            notification_id = self._notification_map[key]
            notifications.append({
                'namespaceName' : key,
                'notificationId': notification_id
            })

        r = requests.get(url=url, params={
            'appId'        : self.appId,
            'cluster'      : self.cluster,
            'notifications': json.dumps(notifications, ensure_ascii=False)
        }, timeout=self.timeout)

        apollo_logger.debug('Long polling returns %d: url=%s', r.status_code, r.request.url)

        if r.status_code == 304:
            # no change, loop
            apollo_logger.debug('No change, loop...')
            print("no change, loop...")
            return

        if r.status_code == 200:
            data = r.json()

            print("something changed, {}".format(str(data)))

            for entry in data:
                ns = entry['namespaceName']
                nid = entry['notificationId']
                apollo_logger.info("%s has changes: notificationId=%d", ns, nid)
                self._uncached_http_get(ns)
                self._notification_map[ns] = nid
        else:
            apollo_logger.warn('Sleep...')
            time.sleep(self.timeout)

    def _listener(self):
        apollo_logger.info('Entering listener loop...')
        while not self._stopping:
            try:
                self._long_poll()
            except Exception as e:
                apollo_logger.error(e.message)
                time.sleep(1)

        apollo_logger.info("Listener stopped!")
        self.stopped = True


if __name__ == '__main__':
    client = ApolloClient(app_id=1001, config_server_url='http://192.168.1.220:8080', cluster='cluster_bj').start(use_eventlet=False)
    while True:
        if sys.version_info[0] < 3:
            key = raw_input('Enter "quit" to quit...\n')
        else:
            key = input('Enter "quit" to quit...\n')

        if key.lower() == 'quit':
            break

        print(client.get_value(key=key, default_val='none'))

    client.stop()
