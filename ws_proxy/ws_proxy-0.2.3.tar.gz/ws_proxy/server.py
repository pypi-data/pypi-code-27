# coding: utf8

from geventwebsocket.server import WebSocketServer
from netkit.box import Box

from .connection import Connection


class Server(object):

    box_class = Box
    connection_class = Connection

    backend_addr = None

    def wsgi_app(self, environ, start_response):
        return self.connection_class(self).handle(environ, start_response)

    def run(self, proxy_addr, backend_addr, ssl_context=None):
        self.backend_addr = backend_addr
        kwargs = dict()
        if ssl_context is not None:
            kwargs['ssl_context'] = ssl_context

        server = WebSocketServer(
            proxy_addr,
            self.wsgi_app,
            **kwargs
        )

        server.serve_forever()
