# -*- coding: utf-8 -*-

"""
    tests.controllers.test_fund_controller

    This file was automatically generated for Tango Card, Inc. by APIMATIC v2.0 ( https://apimatic.io ).
"""

import jsonpickle
import dateutil.parser
from .controller_test_base import ControllerTestBase
from ..test_helper import TestHelper
from raas.api_helper import APIHelper
from raas.models.deposit_request_model import DepositRequestModel


class FundControllerTests(ControllerTestBase):

    @classmethod
    def setUpClass(cls):
        super(FundControllerTests, cls).setUpClass()
        cls.controller = cls.api_client.fund

    # Tests retrieving deposit information
    def test_test_get_deposit(self):
        # Parameters for the API call
        deposit_id = 'RAD-180426-5407'

        # Perform the API call through the SDK function
        result = self.controller.get_deposit(deposit_id)

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 200)
        
        # Test whether the captured response is as we expected
        self.assertIsNotNone(result)
        expected_body = APIHelper.json_deserialize(
            '{"referenceDepositID":"RAD-180426-5407","amount":1.25,"amountCharged":1.29'
            ',"feePercent":3.5,"createdDate":"2018-04-26T18:56:28.28Z","status":"SUCCESS'
            '","accountNumber":"A32386768"}'
            )
        received_body = APIHelper.json_deserialize(self.response_catcher.response.raw_body)
        self.assertTrue(TestHelper.match_body(expected_body, received_body, check_values = True))


    # Tests adding funds to an account
    def test_test_add_funds(self):
        # Parameters for the API call
        body = APIHelper.json_deserialize(
            '{"accountIdentifier":"sdkautotest5","amount":1.25,"creditCardToken":"56ac1'
            'a30-6ba2-4047-9b8c-70f97a5502c5","customerIdentifier":"sdkautotest4"}'
            , DepositRequestModel.from_dictionary)

        # Perform the API call through the SDK function
        result = self.controller.add_funds(body)

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 200)
        
        # Test whether the captured response is as we expected
        self.assertIsNotNone(result)
        expected_body = APIHelper.json_deserialize(
            '{"referenceDepositID":"RAD-180426-5407","amount":1.25,"amountCharged":1.29'
            ',"feePercent":3.5,"createdDate":"2018-04-26T18:56:28.28Z","status":"SUCCESS'
            '","accountNumber":"A32386768"}'
            )
        received_body = APIHelper.json_deserialize(self.response_catcher.response.raw_body)
        self.assertTrue(TestHelper.match_body(expected_body, received_body))


    # Tests retrieving all credit cards for a platform
    def test_test_get_credit_cards(self):

        # Perform the API call through the SDK function
        result = self.controller.get_credit_cards()

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 200)
        
        # Test whether the captured response is as we expected
        self.assertIsNotNone(result)
        expected_body = APIHelper.json_deserialize(
            '[{"customerIdentifier":"sdkautotest4","accountIdentifier":"sdkautotest5","'
            'token":"56ac1a30-6ba2-4047-9b8c-70f97a5502c5","label":"SDK Auto Testing Car'
            'd 1","lastFourDigits":"4444","expirationDate":"2020-01","status":"ACTIVE","'
            'createdDate":"2018-04-26T18:52:17.575Z","activationDate":"2018-04-26T18:52:'
            '17.575Z","contactInformation":[{"fullName":"Test User","emailAddress":"test'
            '@example.com"},{"fullName":"Test Man Two","emailAddress":"test2@example.com'
            '"}],"accountNumber":"A32386768"}]'
            )
        received_body = APIHelper.json_deserialize(self.response_catcher.response.raw_body)
        self.assertTrue(TestHelper.match_body(expected_body, received_body, check_values = True))


    # Tests retrieving a single credit card
    def test_test_get_credit_card(self):
        # Parameters for the API call
        token = '56ac1a30-6ba2-4047-9b8c-70f97a5502c5'

        # Perform the API call through the SDK function
        result = self.controller.get_credit_card(token)

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 200)
        
        # Test whether the captured response is as we expected
        self.assertIsNotNone(result)
        expected_body = APIHelper.json_deserialize(
            '{"customerIdentifier":"sdkautotest4","accountIdentifier":"sdkautotest5","t'
            'oken":"56ac1a30-6ba2-4047-9b8c-70f97a5502c5","label":"SDK Auto Testing Card'
            ' 1","lastFourDigits":"4444","expirationDate":"2020-01","status":"ACTIVE","c'
            'reatedDate":"2018-04-26T18:52:17.575Z","activationDate":"2018-04-26T18:52:1'
            '7.575Z","contactInformation":[{"fullName":"Test User","emailAddress":"test@'
            'example.com"},{"fullName":"Test Man Two","emailAddress":"test2@example.com"'
            '}],"accountNumber":"A32386768"}'
            )
        received_body = APIHelper.json_deserialize(self.response_catcher.response.raw_body)
        self.assertTrue(TestHelper.match_body(expected_body, received_body, check_values = True))


