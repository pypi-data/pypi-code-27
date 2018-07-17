# -*- coding: utf-8 -*-

"""
    raas.models.new_credit_card_model

    This file was automatically generated for Tango Card, Inc. by APIMATIC v2.0 ( https://apimatic.io )
"""


class NewCreditCardModel(object):

    """Implementation of the 'NewCreditCard' model.

    Represents the credit card information required to register a credit card

    Attributes:
        number (string): The credit card number
        expiration (string): The credit card expiration date in YYYY-MM
            format
        verification_number (string): The 3 or 4 digit card security code on
            the back of card

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "number":'number',
        "expiration":'expiration',
        "verification_number":'verificationNumber'
    }

    def __init__(self,
                 number=None,
                 expiration=None,
                 verification_number=None):
        """Constructor for the NewCreditCardModel class"""

        # Initialize members of the class
        self.number = number
        self.expiration = expiration
        self.verification_number = verification_number


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
        number = dictionary.get('number')
        expiration = dictionary.get('expiration')
        verification_number = dictionary.get('verificationNumber')

        # Return an object of this model
        return cls(number,
                   expiration,
                   verification_number)


