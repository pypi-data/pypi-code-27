# -*- coding: utf-8 -*-

"""
    tests.controllers.test_catalog_controller

    This file was automatically generated for Tango Card, Inc. by APIMATIC v2.0 ( https://apimatic.io ).
"""

import jsonpickle
import dateutil.parser
from .controller_test_base import ControllerTestBase
from ..test_helper import TestHelper
from raas.api_helper import APIHelper


class CatalogControllerTests(ControllerTestBase):

    @classmethod
    def setUpClass(cls):
        super(CatalogControllerTests, cls).setUpClass()
        cls.controller = cls.api_client.catalog

    # Tests if we can successfully retrieve a platform's catalog
    def test_test_retrieve_catalog(self):

        # Perform the API call through the SDK function
        result = self.controller.get_catalog()

        # Test response code
        self.assertEquals(self.response_catcher.response.status_code, 200)
        
        # Test whether the captured response is as we expected
        self.assertIsNotNone(result)
        expected_body = APIHelper.json_deserialize(
            '{"catalogName":"TestCatalog","brands":[{"brandKey":"B916708","brandName":"'
            'Amazon.com","disclaimer":"disclaimer","description":"desc","shortDescriptio'
            'n":"short desc","terms":"terms","createdDate":"2016-06-17T16:52:24Z","lastU'
            'pdateDate":"2017-10-23T22:18:51Z","imageUrls":{"80w-326ppi":"https://d30s7y'
            'zk2az89n.cloudfront.net/images/brands/b916708-80w-326ppi.png","130w-326ppi"'
            ':"https://d30s7yzk2az89n.cloudfront.net/images/brands/b916708-130w-326ppi.p'
            'ng","200w-326ppi":"https://d30s7yzk2az89n.cloudfront.net/images/brands/b916'
            '708-200w-326ppi.png","278w-326ppi":"https://d30s7yzk2az89n.cloudfront.net/i'
            'mages/brands/b916708-278w-326ppi.png","300w-326ppi":"https://d30s7yzk2az89n'
            '.cloudfront.net/images/brands/b916708-300w-326ppi.png","1200w-326ppi":"http'
            's://d30s7yzk2az89n.cloudfront.net/images/brands/b916708-1200w-326ppi.png"},'
            '"status":"active","items":[{"utid":"U666425","rewardName":"Amazon.com Gift '
            'Card","currencyCode":"USD","status":"active","valueType":"VARIABLE_VALUE","'
            'rewardType":"gift card","minValue":0.01,"maxValue":2000,"createdDate":"2016'
            '-06-17T17:38:45.294Z","lastUpdateDate":"2017-12-15T01:27:49.607Z","countrie'
            's":["US"]}]},{"brandKey":"B725361","brandName":"AMC Theatres®","disclaimer"'
            ':"discl","description":"desc","shortDescription":"short desc","terms":"term'
            's","createdDate":"2016-06-23T21:53:45Z","lastUpdateDate":"2016-07-25T22:41:'
            '11Z","imageUrls":{"80w-326ppi":"https://d30s7yzk2az89n.cloudfront.net/image'
            's/brands/b725361-80w-326ppi.png","130w-326ppi":"https://d30s7yzk2az89n.clou'
            'dfront.net/images/brands/b725361-130w-326ppi.png","200w-326ppi":"https://d3'
            '0s7yzk2az89n.cloudfront.net/images/brands/b725361-200w-326ppi.png","278w-32'
            '6ppi":"https://d30s7yzk2az89n.cloudfront.net/images/brands/b725361-278w-326'
            'ppi.png","300w-326ppi":"https://d30s7yzk2az89n.cloudfront.net/images/brands'
            '/b725361-300w-326ppi.png","1200w-326ppi":"https://d30s7yzk2az89n.cloudfront'
            '.net/images/brands/b725361-1200w-326ppi.png"},"status":"active","items":[{"'
            'utid":"U154092","rewardName":"AMC® Gift Card $10.00","currencyCode":"USD","'
            'status":"active","valueType":"FIXED_VALUE","rewardType":"gift card","faceVa'
            'lue":10,"createdDate":"2016-07-27T02:54:30.142Z","lastUpdateDate":"2016-09-'
            '21T20:59:01.874Z","countries":["US"]},{"utid":"U913336","rewardName":"AMC® '
            'Gift Card $25.00","currencyCode":"USD","status":"active","valueType":"FIXED'
            '_VALUE","rewardType":"gift card","faceValue":25,"createdDate":"2016-07-27T0'
            '2:55:37.899Z","lastUpdateDate":"2016-10-17T20:55:00.386Z","countries":["US"'
            ']},{"utid":"U652361","rewardName":"AMC® Gift Card $50.00","currencyCode":"U'
            'SD","status":"active","valueType":"FIXED_VALUE","rewardType":"gift card","f'
            'aceValue":50,"createdDate":"2016-07-27T02:56:53.391Z","lastUpdateDate":"201'
            '6-09-21T20:59:16.283Z","countries":["US"]}]}]}'
            )
        received_body = APIHelper.json_deserialize(self.response_catcher.response.raw_body)
        self.assertTrue(TestHelper.match_body(expected_body, received_body))


