# -*- coding: utf-8 -*-

"""
    raas.models.full_name_email_model

    This file was automatically generated for Tango Card, Inc. by APIMATIC v2.0 ( https://apimatic.io )
"""


class FullNameEmailModel(object):

    """Implementation of the 'FullNameEmail' model.

    Represents a full name and an email address

    Attributes:
        full_name (string): The full name
        email_address (string): The email address

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "full_name":'fullName',
        "email_address":'emailAddress'
    }

    def __init__(self,
                 full_name=None,
                 email_address=None):
        """Constructor for the FullNameEmailModel class"""

        # Initialize members of the class
        self.full_name = full_name
        self.email_address = email_address


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
        full_name = dictionary.get('fullName')
        email_address = dictionary.get('emailAddress')

        # Return an object of this model
        return cls(full_name,
                   email_address)


