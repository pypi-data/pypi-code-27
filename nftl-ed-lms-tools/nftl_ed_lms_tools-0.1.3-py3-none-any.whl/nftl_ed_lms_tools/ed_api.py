# -*- coding: utf-8 -*-
"""
Tools for interacting with Ed LMS API.

..codeauthor Grzegorz Pawełczuk <grzegorz.pawelczuk@nftlearning.com>
"""
import json
from enum import Enum
from json import JSONDecodeError

import requests
import logging as log

from abc import ABC
from typing import Any, Dict, Optional
from http.client import responses
from requests import Response, RequestException


class CallType(Enum):
    POST = 1
    GET = 2
    DELETE = 3


OptData = Optional[Dict[str, Any]]
OptStr = Optional[str]


class EdApi(ABC):
    """
    Ed API abstract handler

    Args:
        token: Ed admin bearer token to authorize API calls
        api_url: Ed API base Url
    """

    API_VERSION = "v1"

    def __init__(self, token, api_url):
        # type: (str, OptStr) -> None
        self.api_url = api_url
        if not api_url:
            self.api_url = 'https://rest.edapp.com/'
        self.token = token

    def _get_token(self, token):
        # type: (OptStr) -> str
        """
        Validate token - use provided if available or provide admins one

        Args:
            token: optional users auth token
        Returns:
            Auth token that scan be used
        """
        return token if token else self.token

    @staticmethod
    def _get_data(response):
        # type: (Response)-> OptData
        """
        Universal Response validator

        Args:
            response - :py:class:`requests.Response` object to be validated
        Returns:
            None if data is invalid or Dict[str, Any] when success
        """
        if response.ok:
            try:
                data = response.json()
                log.debug(f'ED response "{data}" from {response.url}')
                return data
            except JSONDecodeError as e:
                error_data = response.content or e
                if error_data:
                    log.error(
                        f'ED API error "{error_data}" from {response.url}')
        else:
            status = response.status_code
            name = responses[status]
            error: str = response.headers.get('x-amzn-errortype') or response.text
            msg = 'HTTP error ED (%s - %s, error: %s) from %s with "%s"' % (
                status, name, error, response.url, response.content)
            log.error(msg)
        return None

    def _call(self, method, data=None, token=None, call_type=CallType.GET):
        # type: (str,Optional[Any],Optional[str],CallType) -> Optional[Any]
        """
        Wrapper for request builder

        Args:
            method: Slack API method name
            data: request parameters
            token: optional users auth token
        Returns:
            data structure that is available in json or None
            when error occurred
        """
        req = self._call_api(
            f'{self.API_VERSION}/%s' % method,
            data,
            token,
            call_type
        )

        if req is not None:
            return self._get_data(req)
        return None

    def _call_api(self, method, data, token=None, call_type=CallType.GET):
        # type: (str,OptData,OptStr,CallType) -> Optional[Response]
        """
        Slack POST request builder

        Args:
            method: Slack API method name
            data: request parameters
            token: optional users auth token
        Returns:
            :py:class:`requests.Response` for provided request
        """
        url = f'{self.api_url}{method}'
        try:
            if call_type == CallType.GET:
                log.info(f'ED Requesting {url} with GET')
                return requests.get(
                    url,
                    headers=self.get_headers(token)
                )
            elif call_type == CallType.POST:
                log.info(f'ED Requesting {url} with POST')
                return requests.post(
                    url,
                    headers=self.get_headers(token),
                    data=bytes(json.dumps(data), 'utf-8')
                )
            elif call_type == CallType.DELETE:
                log.info(f'ED Requesting {url} with DELETE')
                return requests.delete(
                    url,
                    headers=self.get_headers(token),
                    data=bytes(json.dumps(data), 'utf-8')
                )
        except RequestException as e:
            log.error(f'ED Error handling req. "{url}" with an exception: {e}')

        return None

    def get_headers(self, token=None):
        # type: (OptStr)-> Dict[str, str]
        return {
            'Authorization': 'Bearer %s' % self._get_token(token),
            'Content-type': 'application/json; charset=utf-8'
        }
