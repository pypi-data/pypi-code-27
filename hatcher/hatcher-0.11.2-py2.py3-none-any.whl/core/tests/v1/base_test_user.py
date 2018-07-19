from hatcher.core.url_templates import URLS_V1
from hatcher.core.tests.v0.base_test_user import BaseTestUser as BaseTestUserV0


class BaseTestUser(BaseTestUserV0):

    api_version = 1
    urls = URLS_V1
