# -*- coding: utf-8 -*-

"""
    raas.models.order_model

    This file was automatically generated for Tango Card, Inc. by APIMATIC v2.0 ( https://apimatic.io )
"""
from raas.api_helper import APIHelper
import raas.models.currency_breakdown_model
import raas.models.reward_model
import raas.models.name_email_model

class OrderModel(object):

    """Implementation of the 'Order' model.

    Represents the response from a get order call

    Attributes:
        reference_order_id (string): The reference order id
        customer_identifier (string): The customer identifier
        account_identifier (string): The account identifier
        account_number (string): The account number
        amount_charged (CurrencyBreakdownModel): The order's amount
            information
        denomination (CurrencyBreakdownModel): Information about the gift card
            amount
        utid (string): The UTID
        reward_name (string): The reward name
        send_email (bool): Indicates if an email was sent to the recipient
        status (string): The order's status
        created_at (datetime): When the order was placed
        reward (RewardModel): Contains the reward credentials
        sender (NameEmailModel): The sender data
        recipient (NameEmailModel): The recipient data
        etid (string): The email template id
        campaign (string): An optional campaign identifier
        email_subject (string): The subject of the email
        external_ref_id (string): An external reference id
        message (string): A message included with the email
        notes (string): Optional customer notes
        margin_share (CurrencyBreakdownModel): Margin share information

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "reference_order_id":'referenceOrderID',
        "customer_identifier":'customerIdentifier',
        "account_identifier":'accountIdentifier',
        "account_number":'accountNumber',
        "amount_charged":'amountCharged',
        "denomination":'denomination',
        "utid":'utid',
        "reward_name":'rewardName',
        "send_email":'sendEmail',
        "status":'status',
        "created_at":'createdAt',
        "reward":'reward',
        "sender":'sender',
        "recipient":'recipient',
        "etid":'etid',
        "campaign":'campaign',
        "email_subject":'emailSubject',
        "external_ref_id":'externalRefID',
        "message":'message',
        "notes":'notes',
        "margin_share":'marginShare'
    }

    def __init__(self,
                 reference_order_id=None,
                 customer_identifier=None,
                 account_identifier=None,
                 account_number=None,
                 amount_charged=None,
                 denomination=None,
                 utid=None,
                 reward_name=None,
                 send_email=None,
                 status=None,
                 created_at=None,
                 reward=None,
                 sender=None,
                 recipient=None,
                 etid=None,
                 campaign=None,
                 email_subject=None,
                 external_ref_id=None,
                 message=None,
                 notes=None,
                 margin_share=None):
        """Constructor for the OrderModel class"""

        # Initialize members of the class
        self.reference_order_id = reference_order_id
        self.customer_identifier = customer_identifier
        self.account_identifier = account_identifier
        self.account_number = account_number
        self.amount_charged = amount_charged
        self.denomination = denomination
        self.utid = utid
        self.reward_name = reward_name
        self.send_email = send_email
        self.status = status
        self.created_at = APIHelper.RFC3339DateTime(created_at) if created_at else None
        self.reward = reward
        self.sender = sender
        self.recipient = recipient
        self.etid = etid
        self.campaign = campaign
        self.email_subject = email_subject
        self.external_ref_id = external_ref_id
        self.message = message
        self.notes = notes
        self.margin_share = margin_share


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
        denomination = raas.models.currency_breakdown_model.CurrencyBreakdownModel.from_dictionary(dictionary.get('denomination')) if dictionary.get('denomination') else None
        utid = dictionary.get('utid')
        reward_name = dictionary.get('rewardName')
        send_email = dictionary.get('sendEmail')
        status = dictionary.get('status')
        created_at = APIHelper.RFC3339DateTime.from_value(dictionary.get("createdAt")).datetime if dictionary.get("createdAt") else None
        reward = raas.models.reward_model.RewardModel.from_dictionary(dictionary.get('reward')) if dictionary.get('reward') else None
        sender = raas.models.name_email_model.NameEmailModel.from_dictionary(dictionary.get('sender')) if dictionary.get('sender') else None
        recipient = raas.models.name_email_model.NameEmailModel.from_dictionary(dictionary.get('recipient')) if dictionary.get('recipient') else None
        etid = dictionary.get('etid')
        campaign = dictionary.get('campaign')
        email_subject = dictionary.get('emailSubject')
        external_ref_id = dictionary.get('externalRefID')
        message = dictionary.get('message')
        notes = dictionary.get('notes')
        margin_share = raas.models.currency_breakdown_model.CurrencyBreakdownModel.from_dictionary(dictionary.get('marginShare')) if dictionary.get('marginShare') else None

        # Return an object of this model
        return cls(reference_order_id,
                   customer_identifier,
                   account_identifier,
                   account_number,
                   amount_charged,
                   denomination,
                   utid,
                   reward_name,
                   send_email,
                   status,
                   created_at,
                   reward,
                   sender,
                   recipient,
                   etid,
                   campaign,
                   email_subject,
                   external_ref_id,
                   message,
                   notes,
                   margin_share)


