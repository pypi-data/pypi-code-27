# -*- coding: utf-8 -*-

"""
    raas.models.unregister_credit_card_response_model

    This file was automatically generated for Tango Card, Inc. by APIMATIC v2.0 ( https://apimatic.io )
"""
from raas.api_helper import APIHelper

class UnregisterCreditCardResponseModel(object):

    """Implementation of the 'UnregisterCreditCardResponse' model.

    Represents the response from the unregister credit card call

    Attributes:
        created_date (datetime): The date the card was removed
        message (string): A message describing the status of the card
        token (string): The credit card token

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "created_date":'createdDate',
        "message":'message',
        "token":'token'
    }

    def __init__(self,
                 created_date=None,
                 message=None,
                 token=None):
        """Constructor for the UnregisterCreditCardResponseModel class"""

        # Initialize members of the class
        self.created_date = APIHelper.RFC3339DateTime(created_date) if created_date else None
        self.message = message
        self.token = token


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
        created_date = APIHelper.RFC3339DateTime.from_value(dictionary.get("createdDate")).datetime if dictionary.get("createdDate") else None
        message = dictionary.get('message')
        token = dictionary.get('token')

        # Return an object of this model
        return cls(created_date,
                   message,
                   token)


