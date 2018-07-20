"""Message objects that represents HTTP messages."""

__all__ = ['HTTPMessage', 'HTTPRequestMessage', 'HTTPResponseMessage']

import cgi
import codecs
import http.client
import http.cookies
import io
import urllib.parse
import wsgiref.headers

from http import HTTPStatus

from . import errors
from . import utils


class HTTPMessage:
    """Represents an HTTP message."""
    default_charset = 'utf-8'
    default_version = '1.1'
    headers_class = wsgiref.headers.Headers


class HTTPRequestMessage(HTTPMessage):
    """Represents an HTTP request message."""

    max_content_length = 0  # unlimited

    __slots__ = ('_url', '_method', '_version', '_scheme', '_headers',
                 '_data', '_cookies', '_form', '_parsed_url', '_parsed_query')

    def __init__(self, url, method, version, scheme, headers, data):
        self._url = url
        self._method = method
        self._version = version
        self._scheme = scheme
        self._headers = self.headers_class(headers)
        self._data = data
        self._cookies = None
        self._form = None
        self._parsed_url = None
        self._parsed_query = None

    @property
    def url(self):
        """Return the full request URL, including query string."""
        return self._url

    @property
    def parsed_url(self):
        """Return the parsed result of the request URL.

        The return value is a namedtuple of six components:
        `scheme`, `netloc`, `path`, `params`, `query`, `fragment`,
        which corresponds to the general structure of a URL:
        `scheme://netloc/path;parameters?query#fragment`.
        """
        if self._parsed_url is None:
            self._parsed_url = urllib.parse.urlparse(self._url)
        return self._parsed_url

    @property
    def method(self):
        """Return the method of the request, e.g., 'GET', 'POST'."""
        return self._method

    @property
    def scheme(self):
        """Return the scheme of the request URL, e.g., 'http', 'https'."""
        return self._scheme

    @property
    def netloc(self):
        """Return the network location part of the request URL, i.e., the
        hostname and port (if present).
        """
        return self.parsed_url.netloc

    @property
    def path(self):
        """Return the path component of the request URL, including query
        string.
        """
        return self.parsed_url.path

    @property
    def query_string(self):
        """Return the query component of the request URL as string."""
        return self.parsed_url.query

    @property
    def parsed_query(self):
        """Return a dictionary with the parsed result of the query string.

         The dictionary keys are the unique query variable names and the
         values are lists of values for each name.
         """
        if self._parsed_query is None:
            self._parsed_query = urllib.parse.parse_qs(self.parsed_url.query)
        return self._parsed_query

    @property
    def host(self):
        """Return the hostname component of the request URL, without port
        number.
        """
        host = self._headers.get('Host').split(':')[0]
        if not host:
            host = self.netloc.split(':')[0]
        return host

    @property
    def port(self):
        """Return the port number of the request URL as integer."""
        port = self._headers.get('Host').split(':')[1]
        if not port:
            port = self.netloc.split(':')[1]
        if not port:
            if self._scheme == 'https':
                port = http.client.HTTPS_PORT
            else:
                port = http.client.HTTP_PORT
        return int(port)

    @property
    def version(self):
        """Return the protocol version of the request, e.g., '1.1'."""
        return self._version

    @property
    def version_tuple(self):
        """Return the protocol version as a 2-tuple of integers.

        For example, if the protocol version is '1.1', the tuple returned
        will be (1, 1), both elements are integers.
        """
        major, minor = self._version.split('.')
        return int(major), int(minor)

    @property
    def headers(self):
        """Return all header fields of the request."""
        return self._headers

    @property
    def cookies(self):
        """Return cookies of the request."""
        if self._cookies is None:
            data = self._headers.get('Cookie')
            if data is not None:
                c = http.cookies.SimpleCookie()
                c.load(data)
                self._cookies = {k: v.value for k, v in c.items()}
            else:
                self._cookies = {}
        return self._cookies

    @property
    def form(self):
        """Return form data of a `POST` request."""
        if self._form is not None:
            return self._form

        self._form = {}

        method = self.method
        if method != 'POST':
            return self._form

        content_type = self.headers.get('Content-Type')
        if content_type not in (
                "multipart/form-data",
                "application/x-www-form-urlencoded"):
            return self._form

        content_length = len(self._data)
        if (self.max_content_length and content_length and
                content_length > self.max_content_length):
            raise errors.RequestEntityTooLarge

        supported_transfer_encoding = ('base64', 'quoted-printable')

        cte = self.headers.get('Content-Transfer-Encoding')
        if cte is not None and cte.lower() not in supported_transfer_encoding:
            raise ValueError(
                'Unsupported content transfer encoding {!r}'.format(cte))

        fs = cgi.FieldStorage(
            fp=io.BytesIO(self._data),
            environ={'REQUEST_METHOD': method,
                     'CONTENT_TYPE': content_type,
                     'CONTENT_LENGTH': str(content_length)},
            keep_blank_values=True)

        if fs.list is None:
            return self._form

        form_fields = []

        for item in fs.list:
            if getattr(item, 'filename') is None:
                value = item.value
                if not isinstance(value, list):
                    form_fields.append((item.name, value))
                else:
                    form_fields.append((item.name, v) for v in value)

        if cte is None:
            self._form = utils.MultiDict(form_fields)
            return self._form

        form = utils.MultiDict()

        try:
            for name, value in form_fields:
                value = codecs.decode(value, cte)
                form[name] = value
        except Exception:
            raise ValueError(
                'Invalid content transfer encoding {}'.format(cte))

        self._form = form
        return self._form

    @property
    def is_secure(self):
        """Return True if the request is over an SSL/TLS secure connection,
        False otherwise."""
        return self._scheme == 'https'


class HTTPResponseMessage(HTTPMessage):
    """Represents an HTTP response message."""

    __slots__ = ('_data', '_headers', '_status_code', '_status_phrase',
                 '_status_description', '_version')

    default_status_code = 200
    default_content_type = "text/html; charset=utf-8"

    def __init__(self, data=None, status_code=None, headers=None,
                 content_type=None, version=None, status_phrase=None):

        if status_code is None:
            status_code = self.default_status_code
        elif not isinstance(status_code, int):
            raise TypeError('status_code argument must be integer, '
                            'not {}'.format(type(status_code).__name__))

        self._status_code = status_code

        if status_phrase is None:
            try:
                status_phrase = HTTPStatus(status_code).phrase
            except ValueError:
                status_phrase = 'UNKNOWN'
        elif not isinstance(status_phrase, str):
            raise TypeError('status_phrase argument must be string, '
                            'not {}'.format(type(status_phrase).__name__))

        self._status_phrase = status_phrase

        if version is None:
            version = self.default_version
        elif not isinstance(version, str):
            raise TypeError('version argument must be string, '
                            'not {}'.format(type(version).__name__))

        self._version = version

        if headers is None:
            headers = self.headers_class()
        elif isinstance(headers, self.headers_class):
            pass
        elif not isinstance(headers, list):
            raise TypeError('Headers must be a list of name/value tuples, '
                            'not {}'.format(type(headers).__name__))
        else:
            headers = self.headers_class(headers)

        if content_type is not None:
            headers['Content-Type'] = content_type
        elif 'Content-Type' not in headers:
            headers['Content-Type'] = self.default_content_type

        self._headers = headers

        if data is None:
            data = b''
        elif isinstance(data, str):
            data = data.encode()
        elif not isinstance(data, (bytes, bytearray)):
            raise TypeError('data argument must be str, bytes or bytearray'
                            ', not {}'.format(type(data).__name__))

        self._data = data

        self._status_description = None

    def set_cookie(self, key, value='', path=None, expires=None, max_age=None,
                   domain=None, secure=None, httponly=False):
        """Set a cookie."""
        if not isinstance(key, str):
            raise TypeError('key argument must be a string, '
                            'not {}'.format(type(key).__name__))

        c = http.cookies.SimpleCookie()
        c[key] = value

        if path is not None:
            c[key]['path'] = path
        else:
            c[key]['path'] = '/'
        if expires is not None:
            c[key]['expires'] = expires
        if max_age is not None:
            c[key]['max-age'] = max_age
        if domain is not None:
            c[key]['domain'] = domain
        if secure is not None:
            c[key]['secure'] = secure
        if httponly:
            c[key]['httponly'] = httponly

        self.headers.add_header('Set-Cookie', c[key].OutputString())

    def delete_cookie(self, key):
        """Delete a cookie.

        :param key: the name of the cookie to be deleted.
        """
        self.set_cookie(key, value='', expires=0, max_age=0)

    @property
    def data(self):
        """Return the payload data."""
        return self._data

    @property
    def status_code(self):
        """Return status code of the response message."""
        return self._status_code

    @property
    def status_phrase(self):
        """Return reason phrase of the status code."""
        return self._status_phrase

    @property
    def status_description(self):
        """Return the description of the status code."""
        if self._status_description is None:
            code = self._status_code
            try:
                self._status_description = HTTPStatus(code).description
            except ValueError:
                self._status_description = 'UNKNOWN'
        return self._status_description

    @property
    def headers(self):
        """Return all header fields of the response message."""
        return self._headers

    @property
    def version(self):
        """Return the HTTP version of the response message, e.g., '1.1'."""
        return self._version
