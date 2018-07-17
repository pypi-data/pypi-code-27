# -*- coding: utf-8 -*-

"""
    raas.models.raas_server_error_model

    This file was automatically generated for Tango Card, Inc. by APIMATIC v2.0 ( https://apimatic.io )
"""


class RaasServerErrorModel(object):

    """Implementation of the 'RaasServerError' model.

    Represents a RaaS 5xx Error

    Attributes:
        message (string): The error message
        code (int): The RaaS error code

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "message":'message',
        "code":'code'
    }

    def __init__(self,
                 message=None,
                 code=None):
        """Constructor for the RaasServerErrorModel class"""

        # Initialize members of the class
        self.message = message
        self.code = code


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
        message = dictionary.get('message')
        code = dictionary.get('code')

        # Return an object of this model
        return cls(message,
                   code)


