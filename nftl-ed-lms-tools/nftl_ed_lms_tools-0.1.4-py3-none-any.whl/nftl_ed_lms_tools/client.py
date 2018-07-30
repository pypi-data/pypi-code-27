# -*- coding: utf-8 -*-
"""
Tools for interacting with Ed LMS.

..codeauthor Grzegorz Pawełczuk <grzegorz.pawelczuk@nftlearning.com>
"""
from typing import Optional

from nftl_ed_lms_tools.api.usergroups import Usergroups
from nftl_ed_lms_tools.api.users import Users
from nftl_ed_lms_tools.ed_api import OptStr


class EdClient:
    """
    Ed LMS API wrapper
    Partial implementation of methods that full documentation
    is available here http://developer.edapp.com/
    """

    def __init__(self, token, api_url=None):
        # type: (str, OptStr)-> None
        self._token = token
        self._api_url = api_url
        self._users_api: Optional[Users] = None
        self._usergroups_api: Optional[Usergroups] = None

    def get_users_api(self):
        # type: () -> Users
        """
        Provides Wrapper for methods available in Users category

        """
        if not self._users_api:
            self._users_api = Users(self._token, self._api_url)
        return self._users_api

    def get_usersgroups_api(self):
        # type: () -> Usergroups
        """
        Provides Wrapper for methods available in User groups category

        """
        if not self._usergroups_api:
            self._usergroups_api = Usergroups(self._token, self._api_url)
        return self._usergroups_api
