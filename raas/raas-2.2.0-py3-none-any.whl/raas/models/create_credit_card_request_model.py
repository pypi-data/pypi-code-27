# -*- coding: utf-8 -*-

"""
    raas.models.create_credit_card_request_model

    This file was automatically generated for Tango Card, Inc. by APIMATIC v2.0 ( https://apimatic.io )
"""
import raas.models.new_credit_card_model
import raas.models.billing_address_model
import raas.models.full_name_email_model

class CreateCreditCardRequestModel(object):

    """Implementation of the 'CreateCreditCardRequest' model.

    Represents the request to register a credit card

    Attributes:
        customer_identifier (string): The customer identifier
        account_identifier (string): The account identifier
        label (string): The credit card's label/nickname
        ip_address (string): The IP address of the user registering the card
        credit_card (NewCreditCardModel): A NewCreditCard object
        billing_address (BillingAddressModel): A BillingAddress object
        contact_information (list of FullNameEmailModel): An optional array of
            FullNameEmail objects

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "customer_identifier":'customerIdentifier',
        "account_identifier":'accountIdentifier',
        "label":'label',
        "ip_address":'ipAddress',
        "credit_card":'creditCard',
        "billing_address":'billingAddress',
        "contact_information":'contactInformation'
    }

    def __init__(self,
                 customer_identifier=None,
                 account_identifier=None,
                 label=None,
                 ip_address=None,
                 credit_card=None,
                 billing_address=None,
                 contact_information=None):
        """Constructor for the CreateCreditCardRequestModel class"""

        # Initialize members of the class
        self.customer_identifier = customer_identifier
        self.account_identifier = account_identifier
        self.label = label
        self.ip_address = ip_address
        self.credit_card = credit_card
        self.billing_address = billing_address
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
        label = dictionary.get('label')
        ip_address = dictionary.get('ipAddress')
        credit_card = raas.models.new_credit_card_model.NewCreditCardModel.from_dictionary(dictionary.get('creditCard')) if dictionary.get('creditCard') else None
        billing_address = raas.models.billing_address_model.BillingAddressModel.from_dictionary(dictionary.get('billingAddress')) if dictionary.get('billingAddress') else None
        contact_information = None
        if dictionary.get('contactInformation') != None:
            contact_information = list()
            for structure in dictionary.get('contactInformation'):
                contact_information.append(raas.models.full_name_email_model.FullNameEmailModel.from_dictionary(structure))

        # Return an object of this model
        return cls(customer_identifier,
                   account_identifier,
                   label,
                   ip_address,
                   credit_card,
                   billing_address,
                   contact_information)


