import json
import responses

from hatcher.core.url_templates import URLS_V1


class BroodResponses(object):
    """ Mocked brood responses for the repository tests.

    This class contains methods that will setup the necessary requests
    responses to mock the expected behaviour from brood. Each method
    is named after the related test in the related BaseTestUser
    testcase for V0 entry points.

    """

    def __init__(self, url_handler, user):
        self.url_handler = url_handler
        self.urls = URLS_V1
        self.user = user

    def response(self, path):
        handler = self.url_handler
        return '{scheme}://{host}{path}'.format(
            scheme=handler.scheme, host=handler.host, path=path)

    def test_delete_user(self):
        responses.add(
            responses.DELETE,
            self.response(
                path=self.urls.admin.users.metadata.format(
                    organization_name='acme',
                    email=self.user.email)),
            status=201)

    def test_get_metadata(self, expected):
        responses.add(
            responses.GET,
            self.response(
                path=self.urls.admin.users.metadata.format(
                    organization_name='acme',
                    email=self.user.email)),
            body=json.dumps(expected),
            status=200)
