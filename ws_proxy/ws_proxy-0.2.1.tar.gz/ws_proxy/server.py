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

    def run(self, proxy_addr, backend_addr):
        self.backend_addr = backend_addr

        server = WebSocketServer(
            proxy_addr,
            self.wsgi_app,
        )

        server.serve_forever()
