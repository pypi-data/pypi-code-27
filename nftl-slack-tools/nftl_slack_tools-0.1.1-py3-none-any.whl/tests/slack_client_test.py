# -*- coding: utf-8 -*-
"""
Automated tests for Ed provisioner.

..codeauthor Grzegorz Pawełczuk <grzegorz.pawelczuk@nftlearning.com>
"""
import json

import pytest
import responses
from requests import HTTPError

from nftl_slack_tools.client import SlackClient


@pytest.fixture
def slack_client():
    return SlackClient('xoxp-xxxx')


@pytest.fixture
def broken_url_slack_client():
    return SlackClient('xoxp-xxxx', 'https://example.com/api')


def test_slack_users(broken_url_slack_client):
    # given:
    api1 = broken_url_slack_client.get_users_api()
    api2 = broken_url_slack_client.get_users_api()

    # then:
    assert api1 == api2


@responses.activate
def test_slack_users_info(slack_client):
    # given:
    responses.add(
        method=responses.GET,
        url='https://slack.com/api/users.info',
        body='{"ok":true,"user":{"test":"test"}}',
        status=200,
        content_type='application/json'
    )

    # then:
    assert slack_client.get_users_api().info('UXXX', locale=True)


@responses.activate
def test_slack_users_info_invalid(slack_client):
    # given:
    responses.add(
        method=responses.GET,
        url='https://slack.com/api/users.info',
        body='{"ok":false, "error":"error_key"}',
        status=200,
        content_type='application/json'
    )

    # then:
    assert not slack_client.get_users_api().info('UXXX', locale=True)


@responses.activate
def test_slack_users_info_invalid_network(slack_client):
    # given:
    responses.add(
        method=responses.GET,
        url='https://slack.com/api/users.info',
        body='',
        status=500,
        content_type='application/json'
    )

    # then:
    assert not slack_client.get_users_api().info('UXXX', locale=True)


def test_slack_channels(slack_client):
    # given:
    api1 = slack_client.get_channels_api()
    api2 = slack_client.get_channels_api()

    # then:
    assert api1 == api2


@responses.activate
def test_slack_channels_info(slack_client):
    # given:
    responses.add(
        method=responses.GET,
        url='https://slack.com/api/channels.list',
        body='{"ok":true,"channels":[]}',
        status=200,
        content_type='application/json'
    )

    # then:
    assert isinstance(slack_client.get_channels_api().list(), list)


@responses.activate
def test_slack_channels_create(slack_client):
    # given:
    responses.add(
        method=responses.POST,
        url='https://slack.com/api/channels.create',
        body='{"ok":true,"channel":{}}',
        status=200,
        content_type='application/json'
    )

    # then:
    assert isinstance(slack_client.get_channels_api().create('terefere'), dict)


@responses.activate
def test_slack_channels_invite(slack_client):
    # given:
    responses.add(
        method=responses.POST,
        url='https://slack.com/api/channels.invite',
        body='{"ok":true,"channel":{}}',
        status=200,
        content_type='application/json'
    )

    # then:
    assert isinstance(
        slack_client.get_channels_api().invite('terefere', 'UXXX'), dict)


@responses.activate
def test_slack_channels_channel_info_by_name_valid(slack_client):
    # given:
    _req_channel_info_by_name()

    # then:
    assert isinstance(
        slack_client.get_channels_api().channel_info('cname'), dict)


@responses.activate
def test_slack_channels_channel_info_exception(slack_client):
    # given:
    responses.add(responses.GET, 'https://slack.com/api/channels.list',
                  body=HTTPError('Error'))

    # then:
    assert not slack_client.get_channels_api().list()


@responses.activate
def test_slack_channels_channel_info_by_name_invalid_req(slack_client):
    # given:
    responses.add(
        method=responses.GET,
        url='https://slack.com/api/channels.list',
        body='',
        status=404,
        content_type='application/json'
    )

    # then:
    assert not slack_client.get_channels_api().list()


@responses.activate
def test_slack_channels_channel_info_by_name_invalid(slack_client):
    # given:
    responses.add(
        method=responses.GET,
        url='https://slack.com/api/channels.list',
        body='{"ok":false,"error":"boom!"}',
        status=200,
        content_type='application/json'
    )

    # then:
    assert not slack_client.get_channels_api().channel_info('cname')


@responses.activate
def test_slack_channels_channel_info_by_name_not_found(slack_client):
    # given:
    responses.add(
        method=responses.GET,
        url='https://slack.com/api/channels.list',
        body='{"ok":true,"channels":[{"id":"id","name":"boom"}]}',
        status=200,
        content_type='application/json'
    )

    # then:
    assert not slack_client.get_channels_api().channel_info('cname')


@responses.activate
def test_slack_channels_clear_history(slack_client):
    def _response(has_more: bool = False):
        return {
            'ok': True,
            'has_more': has_more,
            'messages': [{
                'ts': '111',
                'name': channel_name
            }]
        }

    # given:
    channel_name = 'general'
    channel_id = 'xxx'
    api_ = 'https://slack.com/api'
    _req_channel_info_by_name(channel_name)

    responses.add(
        method=responses.GET,
        url='%s/channels.history?channel=%s&count=10'
            % (api_, channel_id),
        body=json.dumps(_response(True)),
        status=200,
        content_type='application/json'
    )

    responses.add(
        method=responses.GET,
        url='%s/channels.history?channel=%s&count=10&latest=%s'
            % (api_, channel_id, '111'),
        body=json.dumps(_response(False)),
        status=200,
        content_type='application/json'
    )

    _req_chat_delete(channel_id)
    _req_chat_delete(channel_id, 'false')
    _req_chat_delete(channel_id)

    # then:
    assert slack_client.get_channels_api().clear_history(
        channel_name,
        slack_client.get_chat_api()
    ) == 2


def _req_channel_info_by_name(name: str = 'cname'):
    responses.add(
        method=responses.GET,
        url='https://slack.com/api/channels.list',
        body='{"ok":true,"channels":[{"id":"xxx","name":"%s"}]}' % name,
        status=200,
        content_type='application/json'
    )


def _req_chat_delete(channel_id: str, ok: str = 'true',
                     base_url: str = 'https://slack.com/api'):
    responses.add(
        method=responses.POST,
        url=('%s/chat.delete' % base_url),
        body='{"ok":%s,"channel":"%s"}' % (ok, channel_id),
        status=200,
        content_type='application/json'
    )
