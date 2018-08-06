import requests_mock

from directory_cms_client import DirectoryCMSClient
from directory_cms_client.version import __version__


def test_cms_client_list_by_page_type_draft():
    client = DirectoryCMSClient(
        base_url='http://example.com',
        api_key='debug',
        sender_id='test-sender',
        timeout=5,
        service_name='foo'
    )
    with requests_mock.mock(case_sensitive=True) as mock:
        mock.get('http://example.com/api/pages/')
        client.list_by_page_type('thing', draft_token='draft-token')
        request = mock.request_history[0]

        assert request.qs == {
            'draft_token': ['draft-token'],
            'fields': ['*'],
            'type': ['thing'],
        }


def test_cms_client_lookup_by_slug_language():
    client = DirectoryCMSClient(
        base_url='http://example.com',
        api_key='debug',
        sender_id='test-sender',
        timeout=5,
        service_name='foo'
    )
    with requests_mock.mock(case_sensitive=True) as mock:
        mock.get('http://example.com/api/pages/lookup-by-slug/thing/')
        client.lookup_by_slug('thing', language_code='de')
        request = mock.request_history[0]

        assert request.qs == {
            'service_name': ['foo'],
            'lang': ['de'],
            'fields': ['*'],
        }


def test_cms_client_lookup_by_slug_draft():
    client = DirectoryCMSClient(
        base_url='http://example.com',
        api_key='debug',
        sender_id='test-sender',
        timeout=5,
        service_name='foo'
    )
    with requests_mock.mock(case_sensitive=True) as mock:
        mock.get('http://example.com/api/pages/lookup-by-slug/thing/')
        client.lookup_by_slug('thing', draft_token='draft-token')
        request = mock.request_history[0]

        assert request.qs == {
            'service_name': ['foo'],
            'draft_token': ['draft-token'],
            'fields': ['*'],
        }


def test_cms_client_lookup_by_slug():
    client = DirectoryCMSClient(
        base_url='http://example.com',
        api_key='debug',
        sender_id='test-sender',
        timeout=5,
        service_name='foo'
    )
    with requests_mock.mock(case_sensitive=True) as mock:
        mock.get('http://example.com/api/pages/lookup-by-slug/thing/')
        client.lookup_by_slug('thing')
        request = mock.request_history[0]

        assert request.qs == {
            'service_name': ['foo'],
            'fields': ['*'],
        }


def test_timeout():
    client = DirectoryCMSClient(
        base_url='http://example.com',
        api_key='debug',
        sender_id='test-sender',
        timeout=5,
        service_name='foo'
    )
    assert client.timeout == 5


def test_sender_id():
    client = DirectoryCMSClient(
        base_url='http://example.com',
        api_key='debug',
        sender_id='test-sender',
        timeout=5,
        service_name='foo'
    )

    assert client.request_signer.sender_id == 'test-sender'


def test_version():
    assert DirectoryCMSClient.version == __version__
