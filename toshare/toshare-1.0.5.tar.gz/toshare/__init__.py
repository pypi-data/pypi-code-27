#!/usr/bin/python
# coding: utf-8
# (c) 2017 Raul Granados <@pollitux>

import urllib3

try:
    import json
except ImportError:
    import simplejson as json

__version__ = '1.0.5'
__author__ = 'Raul Granados'

_credentials = ('', '',)
_apiV = 'v1'
_api_base = 'http://api.tosharehq.xyz/api/{}/'.format(_apiV)


class ToShareError(Exception):
    def __init__(self, error_json):
        super(ToShareError, self).__init__(error_json)
        self.error_json = error_json


class MalformedRequestError(ToShareError):
    pass


class AuthenticationError(ToShareError):
    pass


class ProcessingError(ToShareError):
    pass


class ResourceNotFoundError(ToShareError):
    pass


class ParameterValidationError(ToShareError):
    pass


class ApiError(ToShareError):
    pass


class ToShare:
    """
    Build request toshare API
    """

    def __init__(self):
        self.name = None

    _headers = None

    @classmethod
    def auth_api(cls):
        """
        Login in the api
        :return:
        """
        _client_id, _client_secret = _credentials
        payload = {
            'client_id': _client_id, 'client_secret': _client_secret, 'grant_type': 'client_credentials'
        }
        http = urllib3.PoolManager()
        r = http.request('POST', '{}{}'.format(_api_base, 'auth/token'), body=json.dumps(payload))
        if r.status != 200:
            raise ToShareError('Authentication error')
        auth = json.loads(r.data.decode('utf-8'))
        cls._headers = {
            'Authorization': 'Bearer {}'.format(auth['access_token']),
            'content-type': 'application/json',
            'cache-control': 'no-cache',
            'PROJECT-ID': auth['projectId']
        }

    @classmethod
    def build_http_request(cls, method, path, payload=None):
        cls.auth_api()
        method = str(method).lower()
        http = urllib3.PoolManager()

        if method in ('post', 'put'):
            payload = json.dumps(payload).encode('utf-8')
            body = http.request(method, '{}{}'.format(_api_base, path), body=payload, headers=cls._headers)
        else:
            body = http.request(method, '{}{}'.format(_api_base, path), fields=payload, headers=cls._headers)

        response = json.loads(body.data.decode('utf-8'))

        if body.status == 200 or body.status == 201 or body.status == 204:
            response_body = {'status': True}
            try:
                response_body = response
            except Exception:
                pass
            return response_body
        if body.status == 400:
            raise MalformedRequestError(response)
        elif body.status == 401:
            raise AuthenticationError(response)
        elif body.status == 402:
            raise ProcessingError(response)
        elif body.status == 404:
            raise ResourceNotFoundError({'error': response})
        elif body.status == 422:
            raise ParameterValidationError(response)
        elif body.status == 500:
            raise ApiError({'error': response})
        else:
            raise ToShareError({'error': response})

    @classmethod
    def to_object(cls, response):
        for key, value in response.items():
            setattr(cls, key, value)
        return cls

    @classmethod
    def create(cls, data):
        """

        :param data: dict with data for create object
        :return: object with data from response
        """
        return cls.to_object(cls.build_http_request('post', cls.__name__.lower(), data))

    @classmethod
    def retrieve(cls, oid, params=None):
        """

        :params oid: id of object retrieve
        :return: object with data from response
        """
        return cls.to_object(cls.build_http_request('get', '{}/{}'.format(cls.__name__.lower(), oid), payload=params))

    @classmethod
    def all(cls, params=None):
        """
        :type params: extra params for build request
        :return: list of objects from response toshare api
        """
        return cls.build_http_request('get', cls.__name__.lower(), payload=params)

    @classmethod
    def query(cls, params=None):
        """
        :type params: extra params for build request
        :return: list of objects from response toshare api
        """
        return cls.build_http_request('get', cls.__name__.lower(), payload=params)

    @classmethod
    def update(cls, data, oid):
        """
        :param oid: id object
        :type data: data
        :return: object with data from response
        """
        return cls.to_object(cls.build_http_request('put', '{}/{}'.format(cls.__name__.lower(), oid), payload=data))

    @classmethod
    def delete(cls, oid):
        """
        :param oid: id object
        :return: None
        """
        return cls.build_http_request('delete', '{}/{}'.format(cls.__name__.lower(), oid))


class Templates(ToShare):
    """
    Opr with Templates of ToShare API
    """

    @classmethod
    def get(cls, slug):
        """
        :params slug: slug of template
        :return: object with data from response
        """
        t = cls.build_http_request('GET', '{}'.format(cls.__name__.lower()), payload={'slug': slug})
        if len(t) != 1:
            raise ToShareError('Template not fount')
        return cls.to_object(t[0])


class Messages(ToShare):
    """
    Opr with Messages of ToShare API
    """

    @classmethod
    def create(cls, data):
        """
        :param data: dict with data for create object
        :return: object with data from response
        """
        fields_required = ['template', 'data', 'subject', 'fromEmail', 'fromName', 'to']
        for f in fields_required:
            if f not in data:
                raise ToShareError('{} is required'.format(f))
        return cls.to_object(cls.build_http_request('post', cls.__name__.lower(), payload=data))
