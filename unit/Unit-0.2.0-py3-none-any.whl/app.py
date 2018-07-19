"""Web application class."""

__all__ = ['Application']

import asyncio
import functools
import os

from http import HTTPStatus

from . import server
from . import router
from . import utils


class Application:
    """The Web application class.
    
    An Web application is created by creating an instance of this class and
    pass the name of the package as the first parameter. For example:
    
        import unit
        app = unit.Application(__name__)
        
    Then the application object `app` can be used to register routes, error
    handlers, view functions, etc.
    
    Here is a simple `Hello, World!` example with an error handler which
    handles `NOT FOUND` (404) exception:
    
        import unit
        
        app = unit.Application(__name__)
        
        @app.route('/')
        def hello_world(request):
            return 'Hello, World!'
            
        @app.error_handler(404)
        def not_found(request):
            return 'NOT FOUND', 404
        
        if __name__ == '__main__':
            app.run()
    """

    __slots__ = ('package_name', 'package_path', 'router', 'error_handlers',
                 'view_functions', 'static_path', '_loop')

    def __init__(self, package_name, static_path='/static'):
        self.package_name = package_name
        self.package_path = utils.get_package_path(package_name)
        self.router = router.Router()
        self.error_handlers = {}
        self.view_functions = {}
        self.static_path = None

        self._loop = asyncio.get_event_loop()

        # If static_path argument is specified, add support for sending
        # static files (e.g. '*.css', '*.js').
        if static_path:
            self.static_path = os.path.join(
                self.package_path, static_path.lstrip('/'))
            # register route and view function
            self.add_route('__static__', self.static_path + '/<filename>')
            self.view_functions['__static__'] = self._send_static_file

    def add_route(self, name, path, methods=None):
        """Add a route.

        :param name: Name of the route.
        :param path: Path of the route as string.
        :param methods: The request methods a route is limited to, if not
                        specified, 'GET' is set as default'.
        """
        if methods is None:
            methods = ('GET',)
        elif not isinstance(methods, (list, tuple)):
            raise TypeError('methods argument must be a list or tuple, '
                            'not {}'.format(type(methods).__name__))

        self.router.add_route(name, path, methods)

    def route(self, path, methods=None):
        """A decorator for setting up a route.

        This registers the decorated function as a view function and add it
        to `self.view_functions`. By default, the name of the view function
        is used as the name of the route.

        :param path: Path of the route as string.
        :param methods: The request methods a route is limited to, if not
                        specified, 'GET' is set as default'.
        """

        def wrapper(f):
            name = f.__name__
            self.add_route(name, path, methods)
            self.view_functions[name] = f
            return f

        return wrapper

    def error_handler(self, status_code):
        """A decorator registers a function as an error handler.

        :param status_code: Status code of the error.
        """
        if not isinstance(status_code, int):
            raise TypeError('status_code argument must be an integer, '
                            'not {}'.format(type(status_code).__name__))

        def wrapper(f):
            self.error_handlers[status_code] = f
            return f

        return wrapper

    async def _send_static_file(self, request, filename):
        """Send a static file to client.

        :param request: Object that represents the request message.
        :param filename: Name of the static file to send.
        """
        file_path = os.path.join(self.static_path, filename)
        data, ctype, clength = await utils.readfile(file_path, loop=self._loop)
        status_code = HTTPStatus.OK
        headers = [('Content-Type', ctype),
                   ('Content-Length', str(clength))]
        return data, status_code, headers

    def get_handler_factory(self, debug=None):
        """Return a request handler factory object.

        The factory returned is used by the server to create request handler
        object when a request message is received.

        :param debug: Enable debugging if debug is true.
        """
        return functools.partial(server.HTTPRequestHandler,
                                 debug=debug,
                                 loop=self._loop,
                                 router=self.router,
                                 error_handlers=self.error_handlers,
                                 view_functions=self.view_functions)

    def run(self, host=None, port=None, debug=None):
        """Runs an application on a local server.

        :param host: The hostname the server listens on.
        :param port: The port number the server uses.
        :param debug: Enable debugging if debug is true.
        """

        if host is None:
            host = '127.0.0.1'

        if port is None:
            port = 5000

        loop = self._loop

        # Get a request handler factory object
        handler_factory = self.get_handler_factory(debug=debug)

        # Create a local server listening on `host` and `port`
        server = loop.create_server(handler_factory, host=host, port=port)

        # Schedule and run the server
        loop.run_until_complete(server)

        print('> Running on http://{}:{}/\n'
              '  (Press Ctrl-C to stop.)\n'.format(host, port))

        try:
            loop.run_forever()
        except KeyboardInterrupt:  # Ctrl-C pressed
            pass
        finally:
            loop.close()
