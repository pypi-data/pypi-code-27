#! usr/bin/env python3
# -*- coding: utf-8
# rpcserver.py

from multiprocessing.connection import Listener
from multiprocessing.reduction import ForkingPickler
import io
from threading import Thread
import subprocess
import os
import controller

def forking_dumps(obj):
    buf = io.BytesIO()
    ForkingPickler(buf).dump(obj)
    return buf.getvalue()

def forking_loads(obj):
    return ForkingPickler.loads(obj)


class RPCHandler:
    def __init__(self):
        self._functions = { }

    def register_function(self, func):
        if hasattr(func, "__name__"):
            self._functions[func.__name__] = func

    def handle_connection(self, connection):
        try:
            while True:
                # Receive a message
                try:
                    func_name, args, kwargs = forking_loads(connection.recv())
                    # Run the RPC and send a response
                    try:
                        result = self._functions[func_name](*args,**kwargs)
                        connection.send(forking_dumps(result))
                    except Exception as e:
                        connection.send(forking_dumps(e))

                except ConnectionResetError:
                    pass

        except EOFError:
            pass

def rpc_server(handler, address, authkey):
    sock = Listener(address, authkey=authkey)
    while True:
        client = sock.accept()
        t = Thread(target=handler.handle_connection, args=(client,))
        t.daemon = True
        t.start()
        
def connect(**config):
    controller.use_local(**config)
    
def serve_forver(host='localhost', port=17000):
    handler = RPCHandler()
    for call in controller.remote_calls:
        handler.register_function(call)
    rpc_server(handler, (host, port), authkey=b'peekaboo')