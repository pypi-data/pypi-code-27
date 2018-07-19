from hatcher.core.url_templates import URLS_V1
from hatcher.core.tests.v0.base_test_organization import (
    BaseTestOrganization as BaseTestOrganizationV0)


class BaseTestOrganization(BaseTestOrganizationV0):

    api_version = 1
    urls = URLS_V1
