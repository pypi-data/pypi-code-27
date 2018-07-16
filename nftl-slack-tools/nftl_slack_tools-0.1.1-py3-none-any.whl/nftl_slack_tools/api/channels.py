# -*- coding: utf-8 -*-
"""
Tools for interacting with Slack.

..codeauthor Grzegorz Pawełczuk <grzegorz.pawelczuk@nftlearning.com>
"""
import logging as log
from time import sleep
from typing import List, Optional, Dict, Any

from nftl_slack_tools.api.chat import Chat
from nftl_slack_tools.slack_api import SlackApi


class Channels(SlackApi):
    """
    Slack API wrapper that is handling users category
    more info https://api.slack.com/methods#channels
    """
    API_CATEGORY = "channels"

    def __init__(self, slack_token: str, slack_api_url: str = None) -> None:
        super().__init__(slack_token, slack_api_url)

    def list(self, token: Optional[str] = None) -> Optional[List]:
        """
        Lists all channels in a Slack team.
        Channels depends on token so if you want to list users use user token
        instead of SlackApi admin token
        more info https://api.slack.com/methods/channels.list

        Args:
            token: optional auth token that will overwrite SlackApi token
        Returns:
            None if data is invalid or channels :py:class:`typing.List`
            when success
        """
        return super()._call(
            method='list',
            data_key='channels',
            data={'limit': 1000},
            default=[],
            token=token,
            http_get=True
        )

    def create(self, channel: str,
               token: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        Create channel with desired name
        more info https://api.slack.com/methods/channels.create

        Args:
            channel: channel name, can only contain lowercase letters, numbers,
                hyphens, and underscores, and must be 21 characters or less
            token: optional auth token that will overwrite SlackApi token
        Returns:
            None if data is invalid or channel info as :py:class:`typing.Dict`
            when success
        """
        params = {
            'name': channel,
            'validate': True
        }
        return super()._call(
            method='create',
            data_key='channel',
            data=params,
            default={},
            token=token
        )

    def invite(self, channel: str, user: str,
               token: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        Invite user to the channel
        more info https://api.slack.com/methods/channels.invite

        Args:
            channel: Slack channel id like CXJSD234G
            user: Slack user id like UXS65F48
            token: optional auth token that will overwrite SlackApi token
        Returns:
            None if data is invalid or channel info as :py:class:`typing.Dict`
            when success
        """
        params = {'channel': channel, 'user': user}
        return super()._call(
            method='invite',
            data_key='channel',
            data=params,
            default={},
            token=token
        )

    def channel_info(self, channel_name: str,
                     token: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        Find channel info by name
        There is no equivalent method in Slack API

        Args:
            channel_name: Slack channel name
            token: optional auth token that will overwrite SlackApi token
        Returns:
            None if channel_name is not found or channel info
            as :py:class:`typing.Dict` when success
        """
        channels = self.list(token=token)
        if not channels or len(channels) < 1:
            log.error('Channels are unavailable')
            return None

        channel_id = ''
        for channel in channels:
            name = channel.get('name')
            if name and name == channel_name and channel.get('id'):
                return channel
        else:
            log.warning(f'Channel "{channel_id}" not found')
            return None

    def history(self, channel: str, count: int = 100,
                latest: Optional[str] = None,
                token: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        Fetches history of messages and events from a channel.
        more info https://api.slack.com/methods/channels.history

        Args:
            channel: Slack channel id like CXJSD234G
            count: number of msgs per page
            latest: End of time range
            token: optional auth token that will overwrite SlackApi token
        Returns:
            None if error occurred or number of removed messages
        """
        params = {'channel': channel, 'count': f'{count}'}

        if latest:
            params['latest'] = latest

        return super()._call(
            method='history',
            data_key='',
            data=params,
            default=[],
            http_get=True,
            token=token,
            full_response=True
        )

    def clear_history(self, channel_name: str, chat: Chat) -> int:
        """
        Channel history cleaner
        Reads history and removes messages one by one

        Args:
            channel_name: Slack channel name
            chat: chat api handler
        Returns:
            Number of removed messages
        """
        deleted = 0
        channel = self.channel_info(channel_name)
        if channel:
            channel_id: str = channel.get('id', '')
            has_more = True
            msg_id = None
            log.info(f'channel id: "{channel_id}'"")

            while has_more:
                if msg_id:
                    history = self.history(channel_id, 10, msg_id)
                else:
                    history = self.history(channel_id, 10)
                sleep(1.05)
                messages: list = []
                if history:
                    messages = history.get('messages', [])
                    has_more = history.get('has_more', False)

                for msg in messages:
                    msg_id = msg.get('ts')
                    log.info(f'deleting ts {msg_id}')
                    delete = chat.delete(channel_id, msg_id)
                    sleep(0.55)
                    if delete:
                        deleted += 1
                    else:
                        log.warning("throttling break...")
                        sleep(5.05)
                        return deleted + self.clear_history(channel_name, chat)



        return deleted
