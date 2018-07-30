# -*- coding: utf-8 -*-
"""
Tools for interacting with Ed API.

..codeauthor Grzegorz Pawełczuk <grzegorz.pawelczuk@nftlearning.com>
"""
import logging
from typing import Optional, Any, List, Dict

from nftl_ed_lms_tools.ed_api import EdApi, CallType


class Usergroups(EdApi):
    """
    Ed API wrapper that is handling user groups category
    """
    API_VERSION = "v1"

    def __init__(self, token: str, api_url: str = None) -> None:
        super().__init__(token, api_url)

    def get(self, token=None):
        # type: (Optional[str]) -> Optional[List[Any]]
        """
        Get a list of user groups.
        http://developer.edapp.com/#usergroups_get
        Args:
            token: optional auth token that will overwrite EdApi token
        Returns:
            None if data is invalid or user groups info as
            :py:class:`typing.List` when success
        """
        return super()._call(
            method='usergroups',
            token=token,
            call_type=CallType.GET
        )

    def create_or_update_group(self, group_data, token=None):
        # type: (Dict[str,Any], Optional[str]) -> Optional[Dict[str,Any]]
        """
        Create or update a user group.
        http://developer.edapp.com/#usergroups_post

        Args:
            group_data: group data to create or update
            token: optional auth token that will overwrite EdApi token
        Returns:
            None if data is invalid or group info as :py:class:`typing.Dict`
            when success
        """
        if 'id' not in group_data and 'id' not in group_data:
            msg = 'ED group "id" not provided in "{}"'
            logging.error(msg)
            raise AttributeError(msg)

        return super()._call(
            method='usergroups',
            data=group_data,
            token=token,
            call_type=CallType.POST
        )

