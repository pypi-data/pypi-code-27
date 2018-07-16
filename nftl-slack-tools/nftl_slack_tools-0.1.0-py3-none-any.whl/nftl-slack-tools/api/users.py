# -*- coding: utf-8 -*-
"""
Tools for interacting with Slack.

..codeauthor Grzegorz Pawełczuk <grzegorz.pawelczuk@nftlearning.com>
"""
from typing import Optional, Dict, Any

from slack.slack_api import SlackApi


class Users(SlackApi):
    """
    Slack API wrapper that is handling users category
    https://api.slack.com/methods#users
    """
    API_CATEGORY = "users"

    def __init__(self, slack_token: str, slack_api_url: str = None) -> None:
        super().__init__(slack_token, slack_api_url)

    def info(
            self,
            user: str,
            locale: bool = False,
            token: str = None) -> Optional[Dict[str, Any]]:
        """
        Gets information about a user
        more info https://api.slack.com/methods/users.info

        Args:
            user: Slack user id like UXS65F48
            locale: should response contain locale info
            token: optional auth token that will overwrite SlackApi token
        Returns:
            None if data is invalid or user info as :py:class:`typing.Dict`
            when success
        """
        include_locale = 0
        if locale:
            include_locale = 1
        params = {'user': user, 'include_locale': include_locale}
        return super()._call(
            method='info',
            data_key='user',
            data=params,
            default={},
            token=token,
            http_get=True
        )
