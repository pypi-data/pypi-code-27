# -*- coding: utf-8 -*-

"""
takumi_http.utils
~~~~~~~~~~~~~~~~~

Utilities for metadata handling.
"""

import functools
from collections import Mapping

from .session import Session

try:
    import httplib as http_code
except ImportError:
    import http.client as http_code


__all__ = ('http_code', 'Headers', 'Qs', 'HttpMeta', 'pass_request')


class Headers(Mapping):
    """Used to query http headers from context
    """

    PREFIX = '__HEADER__'

    def __init__(self, ctx):
        self.ctx = ctx

    def from_dict(self, dct):
        for k, v in dct.items():
            self.ctx[self._key(k)] = v

    @classmethod
    def _key(cls, key):
        return ''.join([cls.PREFIX, key.lower()])

    def __getitem__(self, key):
        return self.ctx[self._key(key)]

    def __iter__(self):
        for k in self.ctx.keys():
            if not k.startswith(self.PREFIX):
                continue
            yield k.lstrip(self.PREFIX)

    def __len__(self):
        return len([k for k in self.ctx.keys() if k.startswith(self.PREFIX)])


class Qs(Headers):
    """Used to get query string items
    """

    PREFIX = '__QUERY_STRING__'


class HttpMeta(object):
    """For handling http related metadata

    :Example:

    >>> meta = HttpMeta(ctx)
    >>> meta.headers['content-type']
    >>> meta.qs['hello']
    >>> meta.session['hello']

    :param ctx: context holding metadatas
    """
    __slots__ = ('host', 'url', 'method', 'http_version', 'headers', 'qs',
                 'session', 'ctx')

    def __init__(self, ctx):
        self.method = ctx.meta.get('method')
        self.http_version = ctx.meta.get('http_version')
        self.url = ctx.meta.get('url')
        self.host = ctx.meta.get('host')
        self.headers = Headers(ctx.meta)
        self.qs = Qs(ctx.meta)
        self.session = Session.from_cookie(ctx, self.headers.get('cookie', ''))
        self.ctx = ctx


def pass_request(func):
    """Pass request as the first arguments to api handler.

    This decorator can only be used with ``api_with_ctx`` api definition.
    """
    @functools.wraps(func)
    def wrapper(ctx, *args, **kwargs):
        request = HttpMeta(ctx)
        return func(request, *args, **kwargs)
    return wrapper
