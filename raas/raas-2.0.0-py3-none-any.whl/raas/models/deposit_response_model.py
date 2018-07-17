# -*- coding: utf-8 -*-

"""
    raas.models.deposit_response_model

    This file was automatically generated for Tango Card, Inc. by APIMATIC v2.0 ( https://apimatic.io )
"""
from raas.api_helper import APIHelper

class DepositResponseModel(object):

    """Implementation of the 'DepositResponse' model.

    Represents the response from a place deposit call

    Attributes:
        amount (float): The funding amount
        amount_charged (float): The amount charged, after fees
        created_date (datetime): The date the transaction was created
        fee_percent (float): The processing fee percentage
        reference_deposit_id (string): The deposit reference id
        status (string): The status of the transaction

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "amount":'amount',
        "amount_charged":'amountCharged',
        "created_date":'createdDate',
        "fee_percent":'feePercent',
        "reference_deposit_id":'referenceDepositID',
        "status":'status'
    }

    def __init__(self,
                 amount=None,
                 amount_charged=None,
                 created_date=None,
                 fee_percent=None,
                 reference_deposit_id=None,
                 status=None):
        """Constructor for the DepositResponseModel class"""

        # Initialize members of the class
        self.amount = amount
        self.amount_charged = amount_charged
        self.created_date = APIHelper.RFC3339DateTime(created_date) if created_date else None
        self.fee_percent = fee_percent
        self.reference_deposit_id = reference_deposit_id
        self.status = status


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
        amount = dictionary.get('amount')
        amount_charged = dictionary.get('amountCharged')
        created_date = APIHelper.RFC3339DateTime.from_value(dictionary.get("createdDate")).datetime if dictionary.get("createdDate") else None
        fee_percent = dictionary.get('feePercent')
        reference_deposit_id = dictionary.get('referenceDepositID')
        status = dictionary.get('status')

        # Return an object of this model
        return cls(amount,
                   amount_charged,
                   created_date,
                   fee_percent,
                   reference_deposit_id,
                   status)


