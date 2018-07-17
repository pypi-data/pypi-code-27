# -*- coding: utf-8 -*-

"""
    raas.models.account_model

    This file was automatically generated for Tango Card, Inc. by APIMATIC v2.0 ( https://apimatic.io )
"""
from raas.api_helper import APIHelper

class AccountModel(object):

    """Implementation of the 'Account' model.

    Represents an Account

    Attributes:
        account_identifier (string): An account identifier
        account_number (string): An account number
        display_name (string): A display name
        currency_code (string): The currency code for the account
        current_balance (float): The current balance of the account
        created_at (datetime): The date the account was created
        status (string): The status of the account
        contact_email (string): The contact email on file for the account

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "account_identifier":'accountIdentifier',
        "account_number":'accountNumber',
        "display_name":'displayName',
        "currency_code":'currencyCode',
        "current_balance":'currentBalance',
        "created_at":'createdAt',
        "status":'status',
        "contact_email":'contactEmail'
    }

    def __init__(self,
                 account_identifier=None,
                 account_number=None,
                 display_name=None,
                 currency_code='USD',
                 current_balance=None,
                 created_at=None,
                 status=None,
                 contact_email=None):
        """Constructor for the AccountModel class"""

        # Initialize members of the class
        self.account_identifier = account_identifier
        self.account_number = account_number
        self.display_name = display_name
        self.currency_code = currency_code
        self.current_balance = current_balance
        self.created_at = APIHelper.RFC3339DateTime(created_at) if created_at else None
        self.status = status
        self.contact_email = contact_email


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
        account_identifier = dictionary.get('accountIdentifier')
        account_number = dictionary.get('accountNumber')
        display_name = dictionary.get('displayName')
        currency_code = dictionary.get("currencyCode") if dictionary.get("currencyCode") else 'USD'
        current_balance = dictionary.get('currentBalance')
        created_at = APIHelper.RFC3339DateTime.from_value(dictionary.get("createdAt")).datetime if dictionary.get("createdAt") else None
        status = dictionary.get('status')
        contact_email = dictionary.get('contactEmail')

        # Return an object of this model
        return cls(account_identifier,
                   account_number,
                   display_name,
                   currency_code,
                   current_balance,
                   created_at,
                   status,
                   contact_email)


