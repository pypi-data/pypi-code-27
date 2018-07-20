"""Request handler and protocol implementations."""

__all__ = ['HTTPRequestHandler']

import asyncio
import http.server
import inspect

from http import HTTPStatus

from . import errors
from . import message
from . import parser


_UNKNOWN = 'UNKNOWN'


class _Protocol(asyncio.streams.FlowControlMixin, asyncio.Protocol):

    __slots__ = ('_reader', '_writer', '_transport', '_over_ssl')

    def __init__(self, loop=None, reader=None):
        super().__init__(loop=loop)
        self._reader = reader
        self._writer = None
        self._transport = None
        self._over_ssl = False

    @property
    def transport(self):
        return self._transport

    def connection_made(self, transport):
        self._transport = transport
        self._over_ssl = transport.get_extra_info('sslcontext') is not None
        self._writer = asyncio.StreamWriter(transport, self, None, self._loop)

    def connection_lost(self, exc):
        super().connection_lost(exc)
        self._reader = None
        self._writer = None
        self._transport = None

    def data_received(self, data):
        self._reader.feed_data(data)

    def eof_received(self):
        if self._over_ssl:
            # Prevent a warning in SSLProtocol.eof_received:
            # "returning true from eof_received()
            # has no effect when using ssl"
            return False
        return True

    def send(self, data):
        return self._writer.write(data)


class HTTPRequestHandler(_Protocol):

    __slots__ = ('_router', '_error_handlers', '_view_functions',
                 '_keepalive_timeout', '_debug', '_keepalive_handle',
                 '_last_response_time', '_should_keepalive', '_closed')

    # Default keep-alive timeout value
    keepalive_timeout = 5.0

    # Value used for rescheduling the keep-live handle callback
    keepalive_handle_reschedule = 1.0

    # Default class used for representing an HTTP request message
    request_class = message.HTTPRequestMessage

    # Default class used for representing an HTTP response message
    response_class = message.HTTPResponseMessage

    # Default error message template
    error_message_format = http.server.DEFAULT_ERROR_MESSAGE

    def __init__(self, loop=None, router=None, error_handlers=None,
                 view_functions=None, keepalive_timeout=None, debug=None):
        
        loop = asyncio.get_event_loop() if loop is None else loop
        reader = parser.HTTPRequestParser(callback=self.get_request)
        super().__init__(loop=loop, reader=reader)

        self._router = router
        self._error_handlers = error_handlers
        self._view_functions = view_functions

        if keepalive_timeout is None:
            self._keepalive_timeout = self.keepalive_timeout
        else:
            self._keepalive_timeout = float(keepalive_timeout)

        self._debug = debug
        self._keepalive_handle = None
        self._last_response_time = None
        # Set up HTTP/1.1 persistent connection as default
        self._should_keepalive = True
        self._closed = False

    def get_request(self, url, method, version, headers, data):
        """Generate the request object and schedule the handling process.

        This is a callback function called by the request parser when the
        incoming data bytes has been parsed completely.

        :param url: URL of the request message.
        :param method: Method of the request message.
        :param version: Protocol version of the request message.
        :param headers: Header fields of the request message.
        :param data: Payload data of the request message in bytes.
        """
        scheme = 'https' if self._over_ssl else 'http'
        request = self.request_class(
            url, method, version, scheme, headers, data)

        con = request.headers.get('Connection', '').lower()
        if (con == 'close' or
                (version == '1.0' and con != 'keep-alive') or
                version < '1.0'):
                self._should_keepalive = False

        self._loop.create_task(self.handle_request(request))

    async def handle_request(self, request):
        """Start handling a request.

        :param request: Object that represents the request message.
        """
        try:
            # Match request
            value = await self.match_request(request)

            # Prepare response
            if isinstance(value, self.response_class):
                response = value
            else:
                response = self.prepare_response(value)

            # Start response
            await self.start_response(response, request.method)

        finally:
            if self._should_keepalive:
                # Keep the connection persistent
                self._last_response_time = now = self._loop.time()
                self._keepalive_handle = self._loop.call_at(
                    now + self._keepalive_timeout, self.handle_keepalive)
            else:
                # Close the connection
                self.close()

    async def match_request(self, request):
        """Match a request and call the handler function.

        :param request: Object that represents the request message.
        """
        method, url = request.method, request.url
        try:
            func_name, args = await self._router.match(method, url)
            view_func = self._view_functions[func_name]

            if inspect.iscoroutinefunction(view_func):
                return await view_func(request, **args)
            else:
                return view_func(request, **args)

        except errors.HTTPException as exc:
            return await self.handle_error(exc)
        except:
            if self._debug:
                raise
            return await self.handle_error(errors.InternalServerError)  # 500

    def prepare_response(self, value):
        """Generate the response object.

        This converts the return value of `match_request` to an instance
        of `self.response_class`.

        :param value: The value returned from `self.match_request`.
        """
        headers = None
        status_code = None

        if isinstance(value, (str, bytes, bytearray)):
            data = value
        elif isinstance(value, (tuple, list)):
            lv = len(value)
            if lv == 3:
                data, status_code, headers = value
            elif lv == 2:
                data, status_code = value
            elif lv == 1:
                raise TypeError('The tuple/list returned from view function '
                                'has only 1 element, expecting 2 or 3')
            else:
                raise TypeError('Unexpected number of elements returned from '
                                'view function, expecting 2 or 3, '
                                'got {}'.format(lv))
        else:
            raise TypeError('Unexpected value returned from view function '
                            '{}'.format(type(value).__name__))

        return self.response_class(data, status_code, headers)

    async def start_response(self, response, request_method):
        """Start sending a response.

        This writes the response start-line, headers and message body
        (if the body should be sent) to the transport.

        :param response: Object that represents the response message.
        :param request_method: Method of the request message.
        """
        version = response.version
        code = response.status_code
        phrase = response.status_phrase
        start_line = 'HTTP/{} {} {}\r\n'.format(version, code, phrase).encode()
        self.send(start_line)

        data = response.data
        headers = response.headers
        # Message body is omitted for cases described in:
        #  - RFC7230 3.3: 1xx, 204 (No Content), 304 (Not Modified)
        #  - RFC7231 6.3.6: 205 (Reset Content)
        if code < 200 or code in (204, 205, 304) or request_method == 'HEAD':
            data = None
        else:
            if data is None:
                data = b''

            # RFC7231 section 3.1.1 says a message containing a payload body
            # SHOULD present a `Content-Type` header field to indicate the
            # media type of the enclosed data.
            if 'Content-Type' not in headers:
                headers['Content-Type'] = 'application/octet-stream'

        # Content-Length header field is omitted for cases described in:
        #  - RFC7230 3.3.2: 1xx, 204 (No Content)
        has_length = 'Content-Length' in headers
        if code < 200 or code == 204:
            if has_length:
                del headers['Content-Length']
        else:
            if data is not None:
                te = [i.lower() for i in headers.get_all('Transfer-Encoding')]
                if 'chunked' in te:
                    if has_length:
                        del headers['Content-Length']
                else:
                    if not has_length:
                        headers['Content-Length'] = str(len(data))

        if 'Connection' not in headers:
            if self._should_keepalive:
                if version == '1.0':
                    headers.add_header('Connection', 'keep-alive')
            else:
                headers.add_header('Connection', 'close')

        self.send(bytes(response.headers))

        if data is not None:
            self.send(data)

    async def handle_error(self, error):
        """Handle an error.

        :param error: The error object to be handled.
        """
        code = error.code

        # If it's a redirect exception, add the 'Location' header
        # with the new URL to the response message.
        if isinstance(error, errors.RedirectException):
            headers = [('Location', error.new_url)]
            return self.response_class(status_code=code, headers=headers)

        # Otherwise, try to find an specified error handler.
        handler = self._error_handlers.get(code)
        if handler is not None:
            if inspect.iscoroutinefunction(handler):
                return await handler(code)
            else:
                return handler(code)

        # If no error handler is found, generate an error message
        # using the default error message template.
        try:
            status = HTTPStatus(code)
            message, explain = status.phrase, status.description
        except ValueError:
            message, explain = _UNKNOWN, _UNKNOWN

        message = self.error_message_format % {
            'code': code,
            'message': message,
            'explain': explain
        }
        return self.response_class(message, code)

    def handle_keepalive(self):
        """Handle keep-alive/persistent connection."""
        if self._closed:
            return

        wait_until = self._last_response_time + self._keepalive_timeout

        if self._loop.time() >= wait_until:
            # Timed out, close the connection.
            self.close()
            return
        else:
            # Reschedule the callback to be called later.
            self._keepalive_handle = self._loop.call_later(
                self.keepalive_handle_reschedule, self.handle_keepalive)

    def close(self):
        """Close the connection."""
        if self._closed:
            return
        self._transport.close()
        self._transport = None
        self._closed = True
