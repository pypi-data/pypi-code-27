#! /usr/bin/env python3

import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from multiprocessing.reduction import ForkingPickler
from multiprocessing.connection import Client
import io

def forking_dumps(obj):
    buf = io.BytesIO()
    ForkingPickler(buf).dump(obj)
    return buf.getvalue()

def forking_loads(obj):
    return ForkingPickler.loads(obj)


class RPCProxy:
    def __init__(self, connection):
        self._connection = connection

    def __getattr__(self, name):
        def do_rpc(*args, **kwargs):
            try:
                self._connection.send(forking_dumps((name, args, kwargs)))
                result = forking_loads(self._connection.recv())
            except ConnectionResetError:
                result = forking_loads(forking_dumps(b"Probably the server is down!"))

            if isinstance(result, Exception):
                raise result
            return result
        return do_rpc


def Proxy(host, port):
    try:
        client = Client((host, port), authkey = b'peekaboo')
    except ConnectionRefusedError:
        msg="Can't connect to the rpcd server on %s port %s"%(host, port)
        raise ConnectionRefusedError(msg)
    else:
        return RPCProxy(client)
        
if __name__ == "__main__":
    proxy = Proxy()
