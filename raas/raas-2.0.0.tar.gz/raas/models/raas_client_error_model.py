# -*- coding: utf-8 -*-

"""
    raas.models.raas_client_error_model

    This file was automatically generated for Tango Card, Inc. by APIMATIC v2.0 ( https://apimatic.io )
"""


class RaasClientErrorModel(object):

    """Implementation of the 'RaasClientError' model.

    Represents a RaaS 4xx Error

    Attributes:
        path (string): The path to the invalid value
        message (string): The error message
        constraint (string): The constraint validated
        invalid_value (string): The value that was invalid

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "path":'path',
        "message":'message',
        "constraint":'constraint',
        "invalid_value":'invalidValue'
    }

    def __init__(self,
                 path=None,
                 message=None,
                 constraint=None,
                 invalid_value=None):
        """Constructor for the RaasClientErrorModel class"""

        # Initialize members of the class
        self.path = path
        self.message = message
        self.constraint = constraint
        self.invalid_value = invalid_value


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
        path = dictionary.get('path')
        message = dictionary.get('message')
        constraint = dictionary.get('constraint')
        invalid_value = dictionary.get('invalidValue')

        # Return an object of this model
        return cls(path,
                   message,
                   constraint,
                   invalid_value)


