# -*- coding: utf-8 -*-

"""
    raas.models.unregister_credit_card_request_model

    This file was automatically generated for Tango Card, Inc. by APIMATIC v2.0 ( https://apimatic.io )
"""


class UnregisterCreditCardRequestModel(object):

    """Implementation of the 'UnregisterCreditCardRequest' model.

    Represents the request to remove a credit card

    Attributes:
        customer_identifier (string): The customer identifier
        account_identifier (string): The account identifier
        credit_card_token (string): The credit card token

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "customer_identifier":'customerIdentifier',
        "account_identifier":'accountIdentifier',
        "credit_card_token":'creditCardToken'
    }

    def __init__(self,
                 customer_identifier=None,
                 account_identifier=None,
                 credit_card_token=None):
        """Constructor for the UnregisterCreditCardRequestModel class"""

        # Initialize members of the class
        self.customer_identifier = customer_identifier
        self.account_identifier = account_identifier
        self.credit_card_token = credit_card_token


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
        customer_identifier = dictionary.get('customerIdentifier')
        account_identifier = dictionary.get('accountIdentifier')
        credit_card_token = dictionary.get('creditCardToken')

        # Return an object of this model
        return cls(customer_identifier,
                   account_identifier,
                   credit_card_token)


