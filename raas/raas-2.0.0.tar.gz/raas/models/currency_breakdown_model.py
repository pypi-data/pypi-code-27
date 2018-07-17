# -*- coding: utf-8 -*-

"""
    raas.models.currency_breakdown_model

    This file was automatically generated for Tango Card, Inc. by APIMATIC v2.0 ( https://apimatic.io )
"""


class CurrencyBreakdownModel(object):

    """Implementation of the 'CurrencyBreakdown' model.

    Represents a breakdown of an amount and currency information

    Attributes:
        currency_code (string): A 3 digit currency code
        exchange_rate (float): The exchange rate
        fee (float): The amount of the fee applied
        total (float): The order total
        value (float): The value of the order

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "currency_code":'currencyCode',
        "exchange_rate":'exchangeRate',
        "fee":'fee',
        "total":'total',
        "value":'value'
    }

    def __init__(self,
                 currency_code=None,
                 exchange_rate=None,
                 fee=None,
                 total=None,
                 value=None):
        """Constructor for the CurrencyBreakdownModel class"""

        # Initialize members of the class
        self.currency_code = currency_code
        self.exchange_rate = exchange_rate
        self.fee = fee
        self.total = total
        self.value = value


    @classmethod
    def from_dictionary(cls,
                        dictionary):
        """Creates an instance of this model from a dictionary

        Args:
            dictionary (dictionary): A dictionary representation of the object as
            obtained from the deserialization of the server's response. The keys
            MUST match property names in the API description.

        Returns:
            object: An instance of this structure class.

        """
        if dictionary is None:
            return None

        # Extract variables from the dictionary
        currency_code = dictionary.get('currencyCode')
        exchange_rate = dictionary.get('exchangeRate')
        fee = dictionary.get('fee')
        total = dictionary.get('total')
        value = dictionary.get('value')

        # Return an object of this model
        return cls(currency_code,
                   exchange_rate,
                   fee,
                   total,
                   value)


