# -*- coding: utf-8 -*-

"""
    tests.controllers.test_accounts_controller

    This file was automatically generated for Tango Card, Inc. by APIMATIC v2.0 ( https://apimatic.io ).
"""

import jsonpickle
import dateutil.parser
from .controller_test_base import ControllerTestBase
from ..test_helper import TestHelper
from raas.api_helper import APIHelper


class AccountsControllerTests(ControllerTestBase):

    @classmethod
    def setUpClass(cls):
        super(AccountsControllerTests, cls).setUpClass()
        cls.controller = cls.api_client.accounts

    # Tests retrieving all accounts under a specific customer
    def test_test_get_all_customer_accounts(self):
        # Parameters for the API call
        customer_identifier = 'sdkautotest1'

        # Perform the API call through the SDK function
        result = self.controller.get_accounts_by_customer(customer_identifier)

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 200)
        
        # Test whether the captured response is as we expected
        self.assertIsNotNone(result)
        expected_body = APIHelper.json_deserialize(
            '[{"accountIdentifier":"sdkautotest3","accountNumber":"A01335766","displayN'
            'ame":"SDK Auto Testing 3","createdAt":"2018-04-26T18:16:51.652Z","status":"'
            'ACTIVE"},{"accountIdentifier":"sdkautotest2","accountNumber":"A11720237","d'
            'isplayName":"SDK Auto Testing 2","createdAt":"2018-04-26T18:13:45.196Z","st'
            'atus":"ACTIVE"}]'
            )
        received_body = APIHelper.json_deserialize(self.response_catcher.response.raw_body)
        self.assertTrue(TestHelper.match_body(expected_body, received_body, check_values = True))


    # Tests retrieving all accounts
    def test_test_get_all_accounts(self):

        # Perform the API call through the SDK function
        result = self.controller.get_all_accounts()

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 200)
        
        # Test whether the captured response is as we expected
        self.assertIsNotNone(result)
        expected_body = APIHelper.json_deserialize(
            '[{"accountIdentifier":"sdkautotest2","accountNumber":"A11720237","displayN'
            'ame":"SDK Auto Testing 2","currencyCode":"USD","currentBalance":0,"createdA'
            't":"2018-04-26T18:13:45.196Z","status":"ACTIVE","contactEmail":"test@exampl'
            'e.com"}]'
            )
        received_body = APIHelper.json_deserialize(self.response_catcher.response.raw_body)
        self.assertTrue(TestHelper.match_body(expected_body, received_body, check_values = True))


    # Tests retrieving a single account
    def test_test_get_single_account(self):
        # Parameters for the API call
        account_identifier = 'sdkautotest2'

        # Perform the API call through the SDK function
        result = self.controller.get_account(account_identifier)

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 200)
        
        # Test whether the captured response is as we expected
        self.assertIsNotNone(result)
        expected_body = APIHelper.json_deserialize(
            '{"accountIdentifier":"sdkautotest2","accountNumber":"A11720237","displayNa'
            'me":"SDK Auto Testing 2","currencyCode":"USD","currentBalance":0,"createdAt'
            '":"2018-04-26T18:13:45.196Z","status":"ACTIVE","contactEmail":"test@example'
            '.com"}'
            )
        received_body = APIHelper.json_deserialize(self.response_catcher.response.raw_body)
        self.assertTrue(TestHelper.match_body(expected_body, received_body, check_values = True))


