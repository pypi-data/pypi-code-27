# -*- coding: utf-8 -*-

"""
    raas.models.credit_card_model

    This file was automatically generated for Tango Card, Inc. by APIMATIC v2.0 ( https://apimatic.io )
"""
from raas.api_helper import APIHelper
import raas.models.full_name_email_model

class CreditCardModel(object):

    """Implementation of the 'CreditCard' model.

    Represents a Credit Card

    Attributes:
        customer_identifier (string): The customer identifier
        account_identifier (string): The account identifier
        token (string): The credit card token
        label (string): The label/nickname for the credit card
        last_four_digits (string): The last four digits of the credit card
            number
        expiration_date (string): The credit card's expiration date
        status (string): The status of the credit card
        created_date (datetime): The date the card was added
        activation_date (datetime): The date the card will be available for
            use
        contact_information (list of FullNameEmailModel): An optional array of
            FullNameEmail objects

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "customer_identifier":'customerIdentifier',
        "account_identifier":'accountIdentifier',
        "token":'token',
        "label":'label',
        "last_four_digits":'lastFourDigits',
        "expiration_date":'expirationDate',
        "status":'status',
        "created_date":'createdDate',
        "activation_date":'activationDate',
        "contact_information":'contactInformation'
    }

    def __init__(self,
                 customer_identifier=None,
                 account_identifier=None,
                 token=None,
                 label=None,
                 last_four_digits=None,
                 expiration_date=None,
                 status=None,
                 created_date=None,
                 activation_date=None,
                 contact_information=None):
        """Constructor for the CreditCardModel class"""

        # Initialize members of the class
        self.customer_identifier = customer_identifier
        self.account_identifier = account_identifier
        self.token = token
        self.label = label
        self.last_four_digits = last_four_digits
        self.expiration_date = expiration_date
        self.status = status
        self.created_date = APIHelper.RFC3339DateTime(created_date) if created_date else None
        self.activation_date = APIHelper.RFC3339DateTime(activation_date) if activation_date else None
        self.contact_information = contact_information


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
        token = dictionary.get('token')
        label = dictionary.get('label')
        last_four_digits = dictionary.get('lastFourDigits')
        expiration_date = dictionary.get('expirationDate')
        status = dictionary.get('status')
        created_date = APIHelper.RFC3339DateTime.from_value(dictionary.get("createdDate")).datetime if dictionary.get("createdDate") else None
        activation_date = APIHelper.RFC3339DateTime.from_value(dictionary.get("activationDate")).datetime if dictionary.get("activationDate") else None
        contact_information = None
        if dictionary.get('contactInformation') != None:
            contact_information = list()
            for structure in dictionary.get('contactInformation'):
                contact_information.append(raas.models.full_name_email_model.FullNameEmailModel.from_dictionary(structure))

        # Return an object of this model
        return cls(customer_identifier,
                   account_identifier,
                   token,
                   label,
                   last_four_digits,
                   expiration_date,
                   status,
                   created_date,
                   activation_date,
                   contact_information)


