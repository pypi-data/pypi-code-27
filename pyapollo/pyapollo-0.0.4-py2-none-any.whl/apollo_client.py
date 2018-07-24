# -*- coding: utf-8 -*-

"""
apollo python client
使用说明: http://wiki.intra.yongqianbao.com/pages/viewpage.action?pageId=11928499
author: sunguangran@daixiaomi.com
"""

import json
import sys
import threading
import time

import requests

from pyapollo.cache.filecache import FileBasedCache


class ApolloProp(object):
    """Apollo配置属性类，用来辅助业务使用配置信息"""

    def __init__(self, client, key, default_val=None, namespace='application', fetch_on_cache_miss=False):
        self.client = client
        self.key = key
        self.default_val = default_val
        self.namespace = namespace
        self.fetch_on_cache_miss = fetch_on_cache_miss

    def value(self):
        return self.client.get_value(key=self.key, default_val=self.default_val, namespace=self.namespace, fetch_on_cache_miss=self.fetch_on_cache_miss)


class ApolloClient(object):

    def __init__(self, app_id, cluster='default', config_server_url='http://localhost:8080', timeout=90, ip=None, file_cache_dir=None):
        self.config_server_url = config_server_url
        self.app_id = app_id
        self.cluster = cluster
        self.timeout = timeout
        self.stopped = False
        self.ip = self.init_ip(ip)

        self.file_cache = FileBasedCache(dir=file_cache_dir) if file_cache_dir else None

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

    def _refresh_cache(self, namespace, value):
        """更新本地文件缓存"""
        if not self.file_cache:
            return

        self.file_cache.refresh(namespace, value)

    def get_value(self, key, default_val=None, namespace='application', fetch_on_cache_miss=False):
        try:
            if namespace not in self._notification_map:
                self._notification_map[namespace] = -1

            if namespace not in self._cache:
                self._cache[namespace] = {}
                self._long_poll()

            if key in self._cache[namespace]:
                return self._cache[namespace][key]

            if fetch_on_cache_miss:
                return self._cached_http_get(key, default_val, namespace)

        except Exception as e:
            print e.message

        if self.file_cache and self.file_cache.exists(namespace):
            cache_cfg = self.file_cache.load(namespace)
            config = cache_cfg['configurations']
            return config[key] if key in config else default_val

        return default_val

    def start(self, use_eventlet=False, eventlet_patch=False):
        """
        Start the long polling loop. Two modes are provided:
        1: thread mode (default), create a worker thread to do the loop. Call self.stop() to quit the loop
        2: eventlet mode (recommended), no need to call the .stop() since it is async
        :param use_eventlet:
        :param eventlet_patch:
        :return:
        """
        if not self._cache:
            self._long_poll()

        if use_eventlet:
            import eventlet
            if eventlet_patch:
                eventlet.monkey_patch()
            eventlet.spawn(self._listener)
        else:
            t = threading.Thread(target=self._listener)
            t.setDaemon(True)
            t.start()

        return self

    def stop(self):
        self._stopping = True

    def _cached_http_get(self, key, default_val, namespace='application'):
        url = '{}/configfiles/json/{}/{}/{}?ip={}'.format(self.config_server_url, self.app_id, self.cluster, namespace, self.ip)
        r = requests.get(url)
        if r.ok:
            data = r.json()
            self._cache[namespace] = data
        else:
            data = self._cache[namespace]

        if key in data:
            return data[key]
        else:
            return default_val

    def _uncached_http_get(self, namespace='application'):
        url = '{}/configs/{}/{}/{}?ip={}'.format(self.config_server_url, self.app_id, self.cluster, namespace, self.ip)
        r = requests.get(url)
        if r.status_code == 200:
            data = r.json()
            self._cache[namespace] = data['configurations']
            print('Updated local cache for namespace {} release key {}: {}'.format(namespace, data['releaseKey'], repr(self._cache[namespace])))

            self._refresh_cache(namespace, data)

    def _long_poll(self):
        url = '{}/notifications/v2'.format(self.config_server_url)
        notifications = []
        for key in self._notification_map:
            notification_id = self._notification_map[key]
            notifications.append({
                'namespaceName' : key,
                'notificationId': notification_id
            })

        try:
            r = requests.get(url=url, params={
                'appId'        : self.app_id,
                'cluster'      : self.cluster,
                'notifications': json.dumps(notifications, ensure_ascii=False)
            }, timeout=self.timeout)

            if r.status_code == 304:
                return

            if r.status_code == 200:
                data = r.json()
                for entry in data:
                    ns = entry['namespaceName']
                    self._uncached_http_get(ns)
                    self._notification_map[ns] = entry['notificationId']
            else:
                time.sleep(self.timeout)
        except Exception as e:
            time.sleep(1)
            print e.message

    def _listener(self):
        while not self._stopping:
            try:
                self._long_poll()
            except Exception as e:
                print e.message
                time.sleep(1)

        self.stopped = True


if __name__ == '__main__':
    client = ApolloClient(app_id=1001, config_server_url='http://192.168.1.220:8080/', file_cache_dir='/Users/sunguangran/tmp/cache').start()
    while True:
        if sys.version_info[0] < 3:
            key = raw_input('Enter "quit" to quit...\n')
        else:
            key = input('Enter "quit" to quit...\n')

        if key.lower() == 'quit':
            break

        prop = ApolloProp(client=client, namespace='application', key=key, default_val="")

        print(prop.value())

    client.stop()
