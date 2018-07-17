# -*- coding: utf-8 -*-

"""
    raas.models.exchange_rate_model

    This file was automatically generated for Tango Card, Inc. by APIMATIC v2.0 ( https://apimatic.io )
"""
from raas.api_helper import APIHelper

class ExchangeRateModel(object):

    """Implementation of the 'ExchangeRate' model.

    Represents an Exchange Rate

    Attributes:
        last_modified_date (datetime): When the exchange rate was last
            updated
        reward_currency (string): The reward currency
        base_currency (string): The base currency
        base_fx (float): The exchange rate

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "last_modified_date":'lastModifiedDate',
        "reward_currency":'rewardCurrency',
        "base_currency":'baseCurrency',
        "base_fx":'baseFx'
    }

    def __init__(self,
                 last_modified_date=None,
                 reward_currency=None,
                 base_currency=None,
                 base_fx=None):
        """Constructor for the ExchangeRateModel class"""

        # Initialize members of the class
        self.last_modified_date = APIHelper.RFC3339DateTime(last_modified_date) if last_modified_date else None
        self.reward_currency = reward_currency
        self.base_currency = base_currency
        self.base_fx = base_fx


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
        last_modified_date = APIHelper.RFC3339DateTime.from_value(dictionary.get("lastModifiedDate")).datetime if dictionary.get("lastModifiedDate") else None
        reward_currency = dictionary.get('rewardCurrency')
        base_currency = dictionary.get('baseCurrency')
        base_fx = dictionary.get('baseFx')

        # Return an object of this model
        return cls(last_modified_date,
                   reward_currency,
                   base_currency,
                   base_fx)


