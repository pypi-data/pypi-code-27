# -*- coding: utf-8 -*-

"""
    raas.models.order_summary_model

    This file was automatically generated for Tango Card, Inc. by APIMATIC v2.0 ( https://apimatic.io )
"""
from raas.api_helper import APIHelper
import raas.models.currency_breakdown_model
import raas.models.name_email_model

class OrderSummaryModel(object):

    """Implementation of the 'OrderSummary' model.

    Represents an Order Summary

    Attributes:
        reference_order_id (string): The reference order id
        customer_identifier (string): The customer identifier
        account_identifier (string): The account identifier
        account_number (string): The account number
        amount_charged (CurrencyBreakdownModel): The order amount information
        margin_share (CurrencyBreakdownModel): The margin share information
        utid (string): The UTID
        reward_name (string): The reward's name
        sender (NameEmailModel): The sender's information
        recipient (NameEmailModel): The recipient's information
        send_email (bool): Indicates if an an email was sent to the recipient
        status (string): The order's status
        created_at (datetime): The date the order was placed
        etid (string): The order's email template id

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "reference_order_id":'referenceOrderID',
        "customer_identifier":'customerIdentifier',
        "account_identifier":'accountIdentifier',
        "account_number":'accountNumber',
        "amount_charged":'amountCharged',
        "margin_share":'marginShare',
        "utid":'utid',
        "reward_name":'rewardName',
        "sender":'sender',
        "recipient":'recipient',
        "send_email":'sendEmail',
        "status":'status',
        "created_at":'createdAt',
        "etid":'etid'
    }

    def __init__(self,
                 reference_order_id=None,
                 customer_identifier=None,
                 account_identifier=None,
                 account_number=None,
                 amount_charged=None,
                 margin_share=None,
                 utid=None,
                 reward_name=None,
                 sender=None,
                 recipient=None,
                 send_email=None,
                 status=None,
                 created_at=None,
                 etid=None):
        """Constructor for the OrderSummaryModel class"""

        # Initialize members of the class
        self.reference_order_id = reference_order_id
        self.customer_identifier = customer_identifier
        self.account_identifier = account_identifier
        self.account_number = account_number
        self.amount_charged = amount_charged
        self.margin_share = margin_share
        self.utid = utid
        self.reward_name = reward_name
        self.sender = sender
        self.recipient = recipient
        self.send_email = send_email
        self.status = status
        self.created_at = APIHelper.RFC3339DateTime(created_at) if created_at else None
        self.etid = etid


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
        reference_order_id = dictionary.get('referenceOrderID')
        customer_identifier = dictionary.get('customerIdentifier')
        account_identifier = dictionary.get('accountIdentifier')
        account_number = dictionary.get('accountNumber')
        amount_charged = raas.models.currency_breakdown_model.CurrencyBreakdownModel.from_dictionary(dictionary.get('amountCharged')) if dictionary.get('amountCharged') else None
        margin_share = raas.models.currency_breakdown_model.CurrencyBreakdownModel.from_dictionary(dictionary.get('marginShare')) if dictionary.get('marginShare') else None
        utid = dictionary.get('utid')
        reward_name = dictionary.get('rewardName')
        sender = raas.models.name_email_model.NameEmailModel.from_dictionary(dictionary.get('sender')) if dictionary.get('sender') else None
        recipient = raas.models.name_email_model.NameEmailModel.from_dictionary(dictionary.get('recipient')) if dictionary.get('recipient') else None
        send_email = dictionary.get('sendEmail')
        status = dictionary.get('status')
        created_at = APIHelper.RFC3339DateTime.from_value(dictionary.get("createdAt")).datetime if dictionary.get("createdAt") else None
        etid = dictionary.get('etid')

        # Return an object of this model
        return cls(reference_order_id,
                   customer_identifier,
                   account_identifier,
                   account_number,
                   amount_charged,
                   margin_share,
                   utid,
                   reward_name,
                   sender,
                   recipient,
                   send_email,
                   status,
                   created_at,
                   etid)


