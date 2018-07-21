import random
from kazoo.client import KazooClient
from kazoo.exceptions import NodeExistsError, NoNodeError

from .config import *

zk = None


def init(zookeeper='127.0.0.1:2181'):
    global zk
    if not zk:
        zk = KazooClient(hosts=zookeeper)
        zk.start()


def register_api(uri, ip, port, env=DEFAULT_ENV, zookeeper=None):
    global zk
    if not zk:
        if zookeeper:
            init(zookeeper)
        else:
            raise RuntimeError('You must init zk first')
    if uri[0] == '/':
        uri = uri[0:]

    path = '/%s/services/%s' % (env, uri)
    # zk.ensure_path(path)
    try:
        zk.create('%s/%s:%s' % (path, ip, port), ('%s:%s' % (ip, port)).encode('utf-8'), makepath=True, ephemeral=True)
        from cutt_sd import checker
        checker.add_services(ip, port, env, uri)
    except NodeExistsError:
        pass


def unregister_api(uri, ip, port, env=DEFAULT_ENV, zookeeper=None):
    global zk
    if not zk:
        if zookeeper:
            init(zookeeper)
        else:
            raise RuntimeError('You must init zk first')
    if uri[0] == '/':
        uri = uri[0:]

    path = '/%s/services/%s' % (env, uri)
    # zk.ensure_path(path)
    try:
        zk.delete('%s/%s:%s' % (path, ip, port))
        from cutt_sd import checker
        checker.remove_services(ip, port, env, uri)
    except NoNodeError:
        pass


def find_api(uri, env=DEFAULT_ENV, zookeeper=None):
    global zk
    if not zk:
        if zookeeper:
            init(zookeeper)
        else:
            raise RuntimeError('You must init zk first')

    if not uri:
        return None

    if uri[0] == '/':
        uri = uri[0:]

    path = '/%s/services/%s' % (env, uri)
    try:
        children = zk.get_children(path)
        if children:
            data, node = zk.get('%s/%s' % (path, random.choice(children)))
            return data.decode('utf-8') if data else None
    except:
        return None
