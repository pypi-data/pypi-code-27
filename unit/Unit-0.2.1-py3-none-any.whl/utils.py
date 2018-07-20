"""Miscellaneous utilities."""

__all__ = ['abort', 'get_package_path', 'readfile', 'redirect', 'MultiDict']

import asyncio
import collections
import concurrent.futures
import mimetypes
import os
import sys

from collections import deque
from http import HTTPStatus

from . import errors


def abort(exc=None):
    """Raise an exception to terminate the transaction.

    If not specified, 'errors.NotFound' (404) is raised by default.

    :param exc: The exception object to raise.
    """
    if exc is None:
        raise errors.NotFound
    elif not isinstance(exc, errors.HTTPException):
        raise ValueError('Invalid exception {!r}'.format(exc))
    else:
        raise exc


def get_package_path(package_name):
    """Get the path of a package from package name.

    :param package_name: The name of the package as string.
    """
    filename = sys.modules[package_name].__file__
    filepath = os.path.dirname(filename)
    return os.path.abspath(filepath)


async def readfile(path, executor=None, loop=None):
    """Read a file asynchronously.

    This reads a file-like object asynchronously by running blocking methods
    in an executor.

    :param path: The absolute path of the file.
    :param executor: The executor object. An instance of
                     `concurrent.futures.ThreadPoolExecutor` is used if
                     executor is None.
    :param loop: An event loop instance. If not specified, the default event
                 loop is used.
    """
    if executor is None:
        executor = concurrent.futures.ThreadPoolExecutor()

    if loop is None:
        loop = asyncio.get_event_loop()

    loop.set_default_executor(executor)
    run_in_executor = loop.run_in_executor

    data = b''
    f = await run_in_executor(None, open, path, 'rb')

    class _Reader:

        def __aiter__(self):
            return self

        async def __anext__(self):
            data = await run_in_executor(None, f.read, 8192)
            if data == b'':
                raise StopAsyncIteration
            return data

    try:
        async for read in _Reader():
            data += read
    finally:
        await run_in_executor(None, f.close)

    # Guess the type of the file based on path.
    mimetype, _ = mimetypes.guess_type(path)

    if mimetype is None:
        content_type = 'application/octet-stream'
    elif mimetype.startswith('text/'):
        content_type = '{}; charset=utf-8'.format(mimetype)
    else:
        content_type = mimetype

    content_length = len(data)
    return data, content_type, content_length


def redirect(new_url, status_code=None):
    """Redirect a request to a new target.

    If `status_code` argument is not specified, the 'errors.Found' (302)
    exception is used by default.

    Supported exceptions are:

      errors.MovedPermanently (301)
      errors.Found (302)
      errors.SeeOther (303)
      errors.TemporaryRedirect (307)

    :param new_url: The new URL to redirect to.
    :param status_code: The status code of the redirect exception.
    """
    if status_code is None:
        exc = errors.Found
    elif not isinstance(status_code, int):
        raise TypeError('status_code argument must be an integer, '
                        'not {}'.format(type(status_code).__name__))
    else:
        exc = {
            HTTPStatus.MOVED_PERMANENTLY: errors.MovedPermanently,
            HTTPStatus.FOUND: errors.Found,
            HTTPStatus.SEE_OTHER: errors.SeeOther,
            HTTPStatus.TEMPORARY_REDIRECT: errors.TemporaryRedirect
        }.get(status_code)

        if exc is None:
            raise ValueError(
                'Unsupported redirection status code {}'.format(status_code))

    exc.new_url = new_url
    raise exc


class MultiDict(dict):
    """A dict subclass that is used to store multiple values for the same key.
    """

    __slots__ = ()

    def __init__(self, *args, **kwargs):

        if len(args) > 1:
            raise TypeError('MultiDict expected at most 1 positional argument,'
                            ' got {}'.format(len(args)))

        mapping = {}

        if args:
            arg = args[0]
            if isinstance(arg, collections.Mapping):
                for key in arg:
                    mapping[key] = deque([arg[key]])
            elif hasattr(arg, 'keys'):
                for key in arg.keys():
                    mapping[key] = deque([arg[key]])
            else:
                for key, value in arg:
                    mapping.setdefault(key, deque()).appendleft(value)

        if kwargs:
            for key, value in kwargs.items():
                mapping.setdefault(key, deque()).append(value)

        super().__init__(mapping)

    def __getitem__(self, key):
        """Get the first value for a key.

        If no such key exists, KeyError is raised.
        """
        try:
            return super().__getitem__(key)[0]
        except (KeyError, IndexError):
            raise KeyError(key)

    def __setitem__(self, key, value):
        """Set the value of a key.

        Note: this does not overwrite an existing value with the same key.
        Use __delitem__() first to delete any existing values.

        The value is added to the left side of the list (deque).
        """
        super().setdefault(key, deque()).appendleft(value)

    def __delitem__(self, key):
        """Delete all values of a key.

        Does not raise an exception if the key is missing.
        """
        try:
            super().__delitem__(key)
        except KeyError:
            pass

    def get(self, key, default=None):
        """Get the first value for a key.

        If no such key exists, `default` is returned.
        """
        try:
            return self[key]
        except KeyError:
            return default

    def get_all(self, key, default=None):
        """Return a list of all values for a key.

        If no such key exists, `default` is returned.
        """
        try:
            return list(super().__getitem__(key))
        except KeyError:
            return default

    def __repr__(self):
        return '{} ({})'.format(self.__class__.__name__, list(self.items()))
