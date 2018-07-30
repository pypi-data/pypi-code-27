# -*- coding: utf-8 -*-
"""
Automated tests for Ed provisioner.

..codeauthor Grzegorz Pawełczuk <grzegorz.pawelczuk@nftlearning.com>
"""
import pytest
import responses
from requests import HTTPError

from nftl_ed_lms_tools.client import EdClient
from nftl_ed_lms_tools.ed_api import EdApi, CallType


@pytest.fixture
def ed_client():
    return EdClient('token')


@pytest.fixture
def broken_url_ed_client():
    return EdClient('token', 'https://example.com/api')


def test_ed_users(broken_url_ed_client):
    # given:
    api1 = broken_url_ed_client.get_users_api()
    api2 = broken_url_ed_client.get_users_api()

    # then:
    assert api1 == api2


def test_ed_user_groups(broken_url_ed_client):
    # given:
    api1 = broken_url_ed_client.get_usergroups_api()
    api2 = broken_url_ed_client.get_usergroups_api()

    # then:
    assert api1 == api2


@responses.activate
def test_ed_get_users(ed_client):
    # given:
    responses.add(
        method=responses.GET,
        url='https://rest.edapp.com/v1/users',
        body='[{"user": "user"}]',
        status=200,
        content_type='application/json'
    )

    # then:
    assert ed_client.get_users_api().get_users()


@responses.activate
def test_ed_get_users_invalid(ed_client):
    # given:
    responses.add(
        method=responses.GET,
        url='https://rest.edapp.com/v1/users',
        body='some <b>html</b>',
        status=200,
        content_type='application/json'
    )

    # then:
    assert not ed_client.get_users_api().get_users()


def test_ed_create_or_update_user_invalid(ed_client, caplog):
    # when :
    with pytest.raises(AttributeError):
        ed_client.get_users_api().create_or_update_user({})

    # then:
    assert 'not provided in user data' in caplog.text


@responses.activate
def test_ed_create_or_update_user(ed_client, caplog):
    # given:
    responses.add(
        method=responses.POST,
        url='https://rest.edapp.com/v1/users',
        body='{"user": "user"}',
        status=200,
        content_type='application/json'
    )

    # then:
    assert ed_client.get_users_api().create_or_update_user({
        'externalIdentifier': 'irrelevant'
    })


@responses.activate
def test_ed_external_token(ed_client):
    # given:
    user = 'irrelevant'
    responses.add(
        method=responses.GET,
        url=f'https://rest.edapp.com/v1/users/external/{user}/token',
        body='{"user": "user"}',
        status=200,
        content_type='application/json'
    )

    # then:
    assert ed_client.get_users_api().get_external_token(user)


@responses.activate
def test_ed_token(ed_client):
    # given:
    user = 'irrelevant'
    responses.add(
        method=responses.GET,
        url=f'https://rest.edapp.com/v1/users/id/{user}/token',
        body='{"user": "user"}',
        status=200,
        content_type='application/json'
    )

    # then:
    assert ed_client.get_users_api().get_token(user)


def test_edapi_response(mocker, caplog):
    # given:
    response = mocker.patch('requests.get').return_value
    response.ok = False
    response.status_code = 500

    # when :
    EdApi._get_data(response)

    # then :
    assert 'HTTP error' in caplog.text


@responses.activate
def test_api_delete(mocker, caplog):
    # given:
    responses.add(responses.GET, 'https://example.com/test',
                  body=HTTPError('Error'))
    api = EdApi('token', 'https://example.com/')

    # when:
    call = api._call('test', None, call_type=CallType.DELETE)

    # then:
    assert not call
    assert 'Error handling req.' in caplog.text


def test_ed_create_or_update_group_invalid(ed_client, caplog):
    # when :
    with pytest.raises(AttributeError):
        ed_client.get_usergroups_api().create_or_update_group({})

    # then:
    assert 'ED group "id" not provided in' in caplog.text


@responses.activate
def test_ed_create_or_update_group(ed_client, caplog):
    # given:
    responses.add(
        method=responses.POST,
        url='https://rest.edapp.com/v1/usergroups',
        body='{"id": "irrelevant"}',
        status=200,
        content_type='application/json'
    )

    # then:
    assert ed_client.get_usergroups_api().create_or_update_group({
        'id': 'irrelevant'
    })


@responses.activate
def test_get_groups(ed_client, caplog):
    # given:
    responses.add(
        method=responses.GET,
        url='https://rest.edapp.com/v1/usergroups',
        body='[{"id": "irrelevant"}]',
        status=200,
        content_type='application/json'
    )

    # then:
    assert ed_client.get_usergroups_api().get()
