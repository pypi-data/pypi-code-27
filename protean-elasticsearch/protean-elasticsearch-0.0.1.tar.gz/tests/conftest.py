"""Module to setup Factories and other required artifacts for tests"""

import pytest


@pytest.fixture(scope='module', autouse=True)
def config():
    """Global Config fixture for all tests"""

    from protean_elasticsearch.config import TestConfig
    return TestConfig()
