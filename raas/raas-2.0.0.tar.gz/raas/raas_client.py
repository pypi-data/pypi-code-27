# -*- coding: utf-8 -*-

"""
    raas.raas_client

    This file was automatically generated for Tango Card, Inc. by APIMATIC v2.0 ( https://apimatic.io ).
"""
from .decorators import lazy_property
from .configuration import Configuration
from .controllers.status_controller import StatusController
from .controllers.accounts_controller import AccountsController
from .controllers.orders_controller import OrdersController
from .controllers.fund_controller import FundController
from .controllers.exchange_rates_controller import ExchangeRatesController
from .controllers.customers_controller import CustomersController
from .controllers.catalog_controller import CatalogController

class RaasClient(object):

    config = Configuration

    @lazy_property
    def status(self):
        return StatusController()

    @lazy_property
    def accounts(self):
        return AccountsController()

    @lazy_property
    def orders(self):
        return OrdersController()

    @lazy_property
    def fund(self):
        return FundController()

    @lazy_property
    def exchange_rates(self):
        return ExchangeRatesController()

    @lazy_property
    def customers(self):
        return CustomersController()

    @lazy_property
    def catalog(self):
        return CatalogController()


    def __init__(self, 
                 platform_name = 'QAPlatform2',
                 platform_key = 'apYPfT6HNONpDRUj3CLGWYt7gvIHONpDRUYPfT6Hj'):
        if platform_name != None:
            Configuration.platform_name = platform_name
        if platform_key != None:
            Configuration.platform_key = platform_key


