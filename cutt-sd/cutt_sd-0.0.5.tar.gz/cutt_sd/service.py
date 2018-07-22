import time

import requests
import socket
from contextlib import closing

from cutt_sd.config import *


def register(uri, port, env=DEFAULT_ENV, sd_server=DEFAULT_SERVER):
    requests.post(sd_server, {
        'action': 'register',
        'port': port,
        'uri': uri,
        'env': env
    })


def unregister(uri, port, env=DEFAULT_ENV, sd_server=DEFAULT_SERVER):
    requests.post(sd_server, {
        'action': 'unregister',
        'port': port,
        'uri': uri,
        'env': env
    })


services_cache = dict()


def find_api(uri, env=DEFAULT_ENV, sd_server=DEFAULT_SERVER):
    global services_cache
    server_key = '%s:%s' % (uri, env)
    if server_key in services_cache:
        ret, t = services_cache[server_key].split('_')
        if time.time() - float(t) < 30:
            return ret

    response = requests.post(sd_server + 'query', {'uri': uri, 'env': env})
    ret = response.text
    if ret:
        with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
            host, port = ret.split(':')
            if sock.connect_ex((host, int(port))) == 0:
                services_cache[server_key] = '%s_%s' % (ret, time.time())
                return ret

    return None
