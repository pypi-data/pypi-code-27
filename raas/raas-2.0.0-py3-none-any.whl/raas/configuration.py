# -*- coding: utf-8 -*-

"""
   raas.configuration

   This file was automatically generated for Tango Card, Inc. by APIMATIC v2.0 ( https://apimatic.io )
"""
import sys
import logging

from .api_helper import APIHelper

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

class Configuration(object):

    """A class used for configuring the SDK by a user.

    This class need not be instantiated and all properties and methods
    are accessible without instance creation.

    """

    # Set the array parameter serialization method
    # (allowed: indexed, unindexed, plain, csv, tsv, psv)
    array_serialization = "indexed"

    # An enum for SDK environments
    class Environment(object):
        # The sandbox environment does not use real money and can be used for testing.
        SANDBOX = 0
        # The production environment uses real money and is for live transactions.
        PRODUCTION = 1

    # An enum for API servers
    class Server(object):
        DEFAULT = 0

    # The environment in which the SDK is running
    environment = Environment.SANDBOX

    # Platform Name (Provided by Tango Card)
    platform_name = 'QAPlatform2'

    # Platform Key (Provided by Tango Card)
    platform_key = 'apYPfT6HNONpDRUj3CLGWYt7gvIHONpDRUYPfT6Hj'

    # All the environments the SDK can run in
    environments = {
        Environment.SANDBOX: {
            Server.DEFAULT: 'https://integration-api.tangocard.com/raas/v2',
        },
        Environment.PRODUCTION: {
            Server.DEFAULT: 'https://api.tangocard.com/raas/v2',
        },
    }

    @classmethod
    def get_base_uri(cls, server=Server.DEFAULT):
        """Generates the appropriate base URI for the environment and the server.

        Args:
            server (Configuration.Server): The server enum for which the base URI is required.

        Returns:
            String: The base URI.

        """
        return cls.environments[cls.environment][server]
