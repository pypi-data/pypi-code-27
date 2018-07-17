# -*- coding: utf-8 -*-

"""
    raas.models.reward_credential_model

    This file was automatically generated for Tango Card, Inc. by APIMATIC v2.0 ( https://apimatic.io )
"""


class RewardCredentialModel(object):

    """Implementation of the 'RewardCredential' model.

    Represents a Reward Credential

    Attributes:
        label (string): The label of the credential
        value (string): The actual credential
        mtype (string): The type of the credential

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "label":'label',
        "value":'value',
        "mtype":'type'
    }

    def __init__(self,
                 label=None,
                 value=None,
                 mtype=None):
        """Constructor for the RewardCredentialModel class"""

        # Initialize members of the class
        self.label = label
        self.value = value
        self.mtype = mtype


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
        label = dictionary.get('label')
        value = dictionary.get('value')
        mtype = dictionary.get('type')

        # Return an object of this model
        return cls(label,
                   value,
                   mtype)


