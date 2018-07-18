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

def Proxy():
    HOST = os.getenv("ECLINIC_HOST", 'localhost')
    PORT = os.getenv("ECLINIC_PORT", 17000)
    try:
        client = Client((HOST, PORT), authkey = b'peekaboo')
    except ConnectionRefusedError:
        msg=("Connection error", "Can't connect to the server on %s port %s"%(HOST, PORT))
        raise SystemExit(msg)
    else:
        return RPCProxy(client)
        
if __name__ == "__main__":
    proxy = Proxy()
