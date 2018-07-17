# -*- coding: utf-8 -*-

"""
    tests.controllers.test_orders_controller

    This file was automatically generated for Tango Card, Inc. by APIMATIC v2.0 ( https://apimatic.io ).
"""

import jsonpickle
import dateutil.parser
from .controller_test_base import ControllerTestBase
from ..test_helper import TestHelper
from raas.api_helper import APIHelper
from raas.models.create_order_request_model import CreateOrderRequestModel


class OrdersControllerTests(ControllerTestBase):

    @classmethod
    def setUpClass(cls):
        super(OrdersControllerTests, cls).setUpClass()
        cls.controller = cls.api_client.orders

    # Tests retrieving a single order
    def test_test_get_order(self):
        # Parameters for the API call
        reference_order_id = 'RA180426-1401-64'

        # Perform the API call through the SDK function
        result = self.controller.get_order(reference_order_id)

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 200)
        
        # Test whether the captured response is as we expected
        self.assertIsNotNone(result)
        expected_body = APIHelper.json_deserialize(
            '{"referenceOrderID":"RA180426-1401-64","customerIdentifier":"sdkautotest4"'
            ',"accountIdentifier":"sdkautotest5","accountNumber":"A32386768","amountChar'
            'ged":{"value":1,"currencyCode":"USD","total":1},"marginShare":{"value":0,"c'
            'urrencyCode":"USD"},"denomination":{"value":1,"currencyCode":"USD"},"utid":'
            '"U561593","rewardName":"Reward Link","sender":{"firstName":"","lastName":""'
            ',"email":""},"recipient":{"email":"","firstName":"","lastName":""},"sendEma'
            'il":false,"status":"COMPLETE","createdAt":"2018-04-26T20:08:59.624Z","rewar'
            'd":{"credentials":{"Redemption URL":"https://sandbox.rewardlink.io/r/1/ed0H'
            'tzSblNV6oFddNnnlf68eXzGQoREvcxwxu_Vi5Wk"},"credentialList":[{"label":"Redem'
            'ption URL","value":"https://sandbox.rewardlink.io/r/1/ed0HtzSblNV6oFddNnnlf'
            '68eXzGQoREvcxwxu_Vi5Wk","type":"url"}],"redemptionInstructions":"<p>&bull; '
            'Click on the redemption link above to activate your Reward Link.<br />\\r'
            '\\n&bull; Next, you will be able to spend your balance on retail gift cards'
            '.</p>\\r\\n\\r\\n<p>If you don&#39;t want to spend your entire Reward Link '
            'value right away, save the email or URL and return via the redemption link '
            '- your value will be waiting to be spent. This allows you to store the bala'
            'nce to redeem at another time.</p>\\r\\n"}}'
            )
        received_body = APIHelper.json_deserialize(self.response_catcher.response.raw_body)
        self.assertTrue(TestHelper.match_body(expected_body, received_body, check_values = True))


    # Tests placing an order with the minimum parameters required
    def test_test_place_order_with_minimum_criteria(self):
        # Parameters for the API call
        body = APIHelper.json_deserialize(
            '{"accountIdentifier":"sdkautotest5","amount":1.00,"customerIdentifier":"sd'
            'kautotest4","sendEmail":false,"utid":"U561593"}'
            , CreateOrderRequestModel.from_dictionary)

        # Perform the API call through the SDK function
        result = self.controller.create_order(body)

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 201)
        
        # Test whether the captured response is as we expected
        self.assertIsNotNone(result)
        expected_body = APIHelper.json_deserialize(
            '{"referenceOrderID":"RA180426-1401-64","customerIdentifier":"sdkautotest4"'
            ',"accountIdentifier":"sdkautotest5","accountNumber":"A32386768","amountChar'
            'ged":{"value":1,"currencyCode":"USD","total":1},"marginShare":{"value":0,"c'
            'urrencyCode":"USD"},"denomination":{"value":1,"currencyCode":"USD"},"utid":'
            '"U561593","rewardName":"Reward Link","sender":{"firstName":"","lastName":""'
            ',"email":""},"recipient":{"email":"","firstName":"","lastName":""},"sendEma'
            'il":false,"status":"COMPLETE","createdAt":"2018-04-26T20:08:59.624Z","rewar'
            'd":{"credentials":{"Redemption URL":"https://sandbox.rewardlink.io/r/1/ed0H'
            'tzSblNV6oFddNnnlf68eXzGQoREvcxwxu_Vi5Wk"},"credentialList":[{"label":"Redem'
            'ption URL","value":"https://sandbox.rewardlink.io/r/1/ed0HtzSblNV6oFddNnnlf'
            '68eXzGQoREvcxwxu_Vi5Wk","type":"url"}],"redemptionInstructions":"<p>&bull; '
            'Click on the redemption link above to activate your Reward Link.<br />\\r'
            '\\n&bull; Next, you will be able to spend your balance on retail gift cards'
            '.</p>\\r\\n\\r\\n<p>If you don&#39;t want to spend your entire Reward Link '
            'value right away, save the email or URL and return via the redemption link '
            '- your value will be waiting to be spent. This allows you to store the bala'
            'nce to redeem at another time.</p>\\r\\n"}}'
            )
        received_body = APIHelper.json_deserialize(self.response_catcher.response.raw_body)
        self.assertTrue(TestHelper.match_body(expected_body, received_body))


