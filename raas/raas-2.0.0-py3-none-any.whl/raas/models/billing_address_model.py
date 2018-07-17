# -*- coding: utf-8 -*-

"""
    raas.models.billing_address_model

    This file was automatically generated for Tango Card, Inc. by APIMATIC v2.0 ( https://apimatic.io )
"""


class BillingAddressModel(object):

    """Implementation of the 'BillingAddress' model.

    Represents a Billing Address

    Attributes:
        first_name (string): The first name
        last_name (string): The last name
        address_line_1 (string): The address
        city (string): The city
        state (string): The state/province
        postal_code (string): The postal code
        country (string): The 2-letter country code
        email_address (string): The billing contact's email address
        address_line_2 (string): An optional second address line

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "first_name":'firstName',
        "last_name":'lastName',
        "address_line_1":'addressLine1',
        "city":'city',
        "state":'state',
        "postal_code":'postalCode',
        "country":'country',
        "email_address":'emailAddress',
        "address_line_2":'addressLine2'
    }

    def __init__(self,
                 first_name=None,
                 last_name=None,
                 address_line_1=None,
                 city=None,
                 state=None,
                 postal_code=None,
                 country=None,
                 email_address=None,
                 address_line_2=None):
        """Constructor for the BillingAddressModel class"""

        # Initialize members of the class
        self.first_name = first_name
        self.last_name = last_name
        self.address_line_1 = address_line_1
        self.city = city
        self.state = state
        self.postal_code = postal_code
        self.country = country
        self.email_address = email_address
        self.address_line_2 = address_line_2


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
        first_name = dictionary.get('firstName')
        last_name = dictionary.get('lastName')
        address_line_1 = dictionary.get('addressLine1')
        city = dictionary.get('city')
        state = dictionary.get('state')
        postal_code = dictionary.get('postalCode')
        country = dictionary.get('country')
        email_address = dictionary.get('emailAddress')
        address_line_2 = dictionary.get('addressLine2')

        # Return an object of this model
        return cls(first_name,
                   last_name,
                   address_line_1,
                   city,
                   state,
                   postal_code,
                   country,
                   email_address,
                   address_line_2)


