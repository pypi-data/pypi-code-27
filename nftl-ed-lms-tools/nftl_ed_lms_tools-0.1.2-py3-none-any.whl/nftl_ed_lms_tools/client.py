# -*- coding: utf-8 -*-
"""
Tools for interacting with Ed LMS.

..codeauthor Grzegorz Pawełczuk <grzegorz.pawelczuk@nftlearning.com>
"""
from typing import Optional

from nftl_ed_lms_tools.api.users import Users


class EdClient:
    """
    Ed LMS API wrapper
    Partial implementation of methods that full documentation
    is available here http://developer.edapp.com/
    """

    def __init__(self, token: str, api_url: str = None) -> None:
        self._token = token
        self._api_url = api_url
        self._users_api: Optional[Users] = None

    def get_users_api(self) -> Users:
        """
        Provides Wrapper for methods available in Users category

        """
        if not self._users_api:
            self._users_api = Users(self._token, self._api_url)
        return self._users_api
