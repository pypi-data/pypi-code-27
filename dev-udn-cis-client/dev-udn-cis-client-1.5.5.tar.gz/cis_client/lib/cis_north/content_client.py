import json
import requests

import urllib3

from cis_client.lib import base_http_client


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class ContentClient(base_http_client.BaseClient):
    def __init__(self, north_host, insecure=False):
        super(ContentClient, self)
        self.north_host = north_host
        self.insecure = insecure

    def get(self, auth_token, ingest_point, content_path, **kwargs):
        endpoint = self.get_endpoint(ingest_point, content_path)
        response = requests.get(
            endpoint,
            verify=(not self.insecure),
            headers={"X-Auth-Token": auth_token},
            params=self.get_auth_params(**kwargs)
        )
        base_http_client.raise_for_http_response(
            response,
            'Getting of content "{content_path}" for "{ingest_point}", brand-id="{brand_id}", '
            'account-id="{account_id}", group-id="{group_id}" was failed.'.format(
                content_path=content_path,
                ingest_point=ingest_point,
                brand_id=kwargs.get('brand_id', ''),
                account_id=kwargs.get('account_id', ''),
                group_id=kwargs.get('group_id', '')
            ))
        return json.loads(response.content)

    def get_endpoint(self, ingest_point, content_path):
        endpoint = '{north_host}/ingest_points/{ingest_point}/content/{content_path}'.format(
            north_host=self.north_host,
            ingest_point=ingest_point,
            content_path=content_path
        )
        return endpoint


@base_http_client.with_auth
def get_content(north_host, ingest_point, content_path, **kwargs):
    """Gets content info

    :param north_host:
    :param ingest_point:
    :param content_path
    :param kwargs: can contains
        - insecure: True if SSL verification must be skipped
        - brand_id: brand ID
        - account_id: account ID
        - group_id: group ID
        - aaa_host: AAA host, optional
        - username: username, optional
        - password: password, optional
        - token: auth token, must be specified if aaa_host,
                 username and password is not specified
    :return: content info
    """
    content_client = ContentClient(north_host, insecure=kwargs['insecure'])
    content_info = content_client.get(kwargs['token'], ingest_point, content_path, **kwargs)
    return content_info
