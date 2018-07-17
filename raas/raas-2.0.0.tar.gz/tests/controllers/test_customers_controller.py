# -*- coding: utf-8 -*-

"""
    tests.controllers.test_customers_controller

    This file was automatically generated for Tango Card, Inc. by APIMATIC v2.0 ( https://apimatic.io ).
"""

import jsonpickle
import dateutil.parser
from .controller_test_base import ControllerTestBase
from ..test_helper import TestHelper
from raas.api_helper import APIHelper


class CustomersControllerTests(ControllerTestBase):

    @classmethod
    def setUpClass(cls):
        super(CustomersControllerTests, cls).setUpClass()
        cls.controller = cls.api_client.customers

    # Tests retrieving all customers
    def test_test_get_all_customers(self):

        # Perform the API call through the SDK function
        result = self.controller.get_all_customers()

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 200)
        
        # Test whether the captured response is as we expected
        self.assertIsNotNone(result)
        expected_body = APIHelper.json_deserialize(
            '[{"customerIdentifier":"sdkautotest1","displayName":"SDK Auto Testing 1","'
            'status":"active","createdAt":"2018-04-26T18:13:12.874Z","accounts":[{"accou'
            'ntIdentifier":"sdkautotest3","accountNumber":"A01335766","displayName":"SDK'
            ' Auto Testing 3","createdAt":"2018-04-26T18:16:51.652Z","status":"ACTIVE"},'
            '{"accountIdentifier":"sdkautotest2","accountNumber":"A11720237","displayNam'
            'e":"SDK Auto Testing 2","createdAt":"2018-04-26T18:13:45.196Z","status":"AC'
            'TIVE"}]}]'
            )
        received_body = APIHelper.json_deserialize(self.response_catcher.response.raw_body)
        self.assertTrue(TestHelper.match_body(expected_body, received_body, check_values = True))


    # Tests retrieving a single customer
    def test_test_get_customer(self):
        # Parameters for the API call
        customer_identifier = 'sdkautotest1'

        # Perform the API call through the SDK function
        result = self.controller.get_customer(customer_identifier)

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 200)
        
        # Test whether the captured response is as we expected
        self.assertIsNotNone(result)
        expected_body = APIHelper.json_deserialize(
            '{"customerIdentifier":"sdkautotest1","displayName":"SDK Auto Testing 1","s'
            'tatus":"active","createdAt":"2018-04-26T18:13:12.874Z","accounts":[{"accoun'
            'tIdentifier":"sdkautotest3","accountNumber":"A01335766","displayName":"SDK '
            'Auto Testing 3","createdAt":"2018-04-26T18:16:51.652Z","status":"ACTIVE"},{'
            '"accountIdentifier":"sdkautotest2","accountNumber":"A11720237","displayName'
            '":"SDK Auto Testing 2","createdAt":"2018-04-26T18:13:45.196Z","status":"ACT'
            'IVE"}]}'
            )
        received_body = APIHelper.json_deserialize(self.response_catcher.response.raw_body)
        self.assertTrue(TestHelper.match_body(expected_body, received_body, check_values = True))


