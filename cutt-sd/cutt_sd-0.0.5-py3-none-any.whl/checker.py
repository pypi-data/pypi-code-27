import socket
import threading
from contextlib import closing
import cutt_sd

servers = dict()


def add_services(ip, port, env, service):
    key = '%s:%s:%s' % (ip, port, env)
    if key not in servers:
        servers[key] = set()

    servers[key].add(service)


def remove_services(ip, port, env, service):
    key = '%s:%s:%s' % (ip, port, env)
    if key not in servers:
        servers[key] = set()

    servers[key].remove(service)

    if len(servers[key]) == 0:
        del servers[key]


def check_all():
    for key, values in servers.items():
        with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
            host, port, env = key.split(':')
            if sock.connect_ex((host, int(port))) == 0:
                pass
            else:
                del servers[key]
                for x in values:
                    cutt_sd.unregister_api(x, host, port, env)


timer = threading.Timer(60, check_all)
timer.daemon = True
timer.start()
