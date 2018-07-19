"""A parser of HTTP request messages."""

__all__ = ['HTTPRequestParser']

import httptools

from . import errors


class HTTPRequestParser(httptools.HttpRequestParser):
    """Parser of HTTP request messages."""

    __slots__ = ('_callback', '_url', '_headers', '_data')

    def __init__(self, callback):
        super().__init__(self)
        self._callback = callback
        self._url = None
        self._headers = []
        self._data = b''

    def feed_data(self, data: bytes):
        """Feed data to the parser.

        :param data: The incoming data in bytes.
        """
        try:
            super().feed_data(data)
        except httptools.HttpParserError:
            raise errors.BadRequest

    def on_url(self, url: bytes):
        """Called when the URL of a request message has been parsed
        successfully.

        :param url: URL of the request message.
        """
        self._url = url.decode()

    def on_header(self, name: bytes, value: bytes):
        """Add a header to the headers buffer.

        :param name: The name of a header field.
        :param value: The value of a header field.
        """
        self._headers.append((name.decode(), value.decode()))

    def on_body(self, data: bytes):
        """Append data to the data buffer.

        :param data: Payload data of the request message.
        """
        self._data += data

    def on_message_complete(self):
        """Called when parsing is completed."""
        try:
            method = super().get_method().decode()
            version = super().get_http_version()
            self._callback(self._url, method, version, self._headers,
                           self._data)
        finally:
            self._cleanup()

    def _cleanup(self):
        """Clean up data associated with the current request message."""
        self._url = None
        self._headers = []
        self._data = b''