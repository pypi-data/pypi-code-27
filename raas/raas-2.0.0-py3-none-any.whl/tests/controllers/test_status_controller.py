# -*- coding: utf-8 -*-

"""
    tests.controllers.test_status_controller

    This file was automatically generated for Tango Card, Inc. by APIMATIC v2.0 ( https://apimatic.io ).
"""

import jsonpickle
import dateutil.parser
from .controller_test_base import ControllerTestBase
from ..test_helper import TestHelper
from raas.api_helper import APIHelper


class StatusControllerTests(ControllerTestBase):

    @classmethod
    def setUpClass(cls):
        super(StatusControllerTests, cls).setUpClass()
        cls.controller = cls.api_client.status

    # Tests if we can retrieve the system status
    def test_test_status_is_ok(self):

        # Perform the API call through the SDK function
        result = self.controller.get_system_status()

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 200)
        
        # Test whether the captured response is as we expected
        self.assertIsNotNone(result)
        expected_body = APIHelper.json_deserialize('{"status":"UP"}')
        received_body = APIHelper.json_deserialize(self.response_catcher.response.raw_body)
        self.assertTrue(TestHelper.match_body(expected_body, received_body))


