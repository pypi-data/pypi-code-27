#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
EDBOWebApiClient
Author: Eldar Aliiev
Email: e.aliiev@vnmu.edu.ua
"""

import re
from . import config as config
from .connector import EDBOWebApiConnector
from .helper import EDBOWebApiHelper
from .methods import EDBOWebApiMethods


class EDBOWebApiClient(EDBOWebApiMethods):
    """EDBOWebApiClient - class which implements some RESTful API methods
    and interface for methods execution by their names.
    """

    def __init__(self, username: str = config.EDBO_USER, password: str = config.EDBO_PASSWORD):
        """Initialize connector and prepare client to work
        :param username: Username (Default=from config file)
        :param password: Method data (Default=from config file)
        :type username: str
        :type password: str
        """
        # Initialize connector
        self._connector = EDBOWebApiConnector(username, password)

        # Get university info
        self._university_info = self._connector.execute('university/list')[0]

    def __getattr__(self, method: str):
        """Call RESTful API method
        :param method: Method of RESTful API
        :type method: str
        :return: Method for execution
        :rtype: function
        """
        # Check if method name is valid
        if re.match(r'([0-9a-z_]+)', method) is not None:

            # Transform method name into url
            url = method.replace('_', '/')

            # Build method wrapper function
            def wrapper(data: dict = None, headers: dict = None, json_format: bool = True):
                # Send request to server
                return self._connector.execute(
                    url,
                    data,
                    headers,
                    json_format
                )

            return wrapper
        else:
            # Fail if method is incorrect
            EDBOWebApiHelper.echo(u'Некоректний метод!', color='red')
            return

    def get_status(self) -> int:
        """Return status of last request
        :return: Status of last method execution
        :rtype: int
        """
        return self._connector.status

    def get_execution_time(self) -> float:
        """Return execution time of last request
        :return: Time of last method execution
        :rtype: float"""
        return self._connector.execution_time

    def get_user_info(self) -> dict:
        """Get information about current user
        :return: Information about current user
        :rtype: dict
        """
        return self._connector.execute('auth/userInfo')

    def get_university_info(self, field: str):
        """Get university info
        :param field: Name of field
        :type field: str
        :return: University info field
        :rtype: str, int
        """
        return self._university_info.get(field, None)


def client() -> EDBOWebApiClient:
    """Return client interface when imported
    :return: Client object
    :rtype: EDBOWebApiClient
    """
    return EDBOWebApiClient()
