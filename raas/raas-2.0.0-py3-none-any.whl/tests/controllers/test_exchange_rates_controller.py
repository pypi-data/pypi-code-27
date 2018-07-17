# -*- coding: utf-8 -*-

"""
    tests.controllers.test_exchange_rates_controller

    This file was automatically generated for Tango Card, Inc. by APIMATIC v2.0 ( https://apimatic.io ).
"""

import jsonpickle
import dateutil.parser
from .controller_test_base import ControllerTestBase
from ..test_helper import TestHelper
from raas.api_helper import APIHelper


class ExchangeRatesControllerTests(ControllerTestBase):

    @classmethod
    def setUpClass(cls):
        super(ExchangeRatesControllerTests, cls).setUpClass()
        cls.controller = cls.api_client.exchange_rates

    # Tests if we can successfully retrieve exchange rates
    def test_test_retrieve_exchange_rates(self):

        # Perform the API call through the SDK function
        result = self.controller.get_exchange_rates()

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 200)
        
        # Test whether the captured response is as we expected
        self.assertIsNotNone(result)
        expected_body = APIHelper.json_deserialize(
            '{"disclaimer":"Exchange rates are provided here for reference. They are up'
            'dated at least once a day and may have changed by time of order.","exchange'
            'Rates":[{"lastModifiedDate":"2018-04-19T13:00:14.291","rewardCurrency":"EUR'
            '","baseCurrency":"NZD","baseFx":0.59120},{"lastModifiedDate":"2018-04-19T13'
            ':00:14.291","rewardCurrency":"USD","baseCurrency":"NZD","baseFx":0.73130},{'
            '"lastModifiedDate":"2018-04-19T13:00:14.230","rewardCurrency":"INR","baseCu'
            'rrency":"AUD","baseFx":51.29066}]}'
            )
        received_body = APIHelper.json_deserialize(self.response_catcher.response.raw_body)
        self.assertTrue(TestHelper.match_body(expected_body, received_body))


