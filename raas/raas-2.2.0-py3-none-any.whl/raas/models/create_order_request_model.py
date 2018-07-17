# -*- coding: utf-8 -*-

"""
    raas.models.create_order_request_model

    This file was automatically generated for Tango Card, Inc. by APIMATIC v2.0 ( https://apimatic.io )
"""
import raas.models.name_email_model

class CreateOrderRequestModel(object):

    """Implementation of the 'CreateOrderRequest' model.

    Represents the request to place an order

    Attributes:
        account_identifier (string): The account identifier
        amount (float): The order amount
        customer_identifier (string): The customer identifier
        send_email (bool): Indicates whether we should deliver this reward via
            email
        utid (string): The UTID
        campaign (string): An optional campaign identifier
        email_subject (string): The subject of the gift email
        external_ref_id (string): An optional external reference id
        message (string): The gift message in the email
        recipient (NameEmailModel): The recipient's information
        sender (NameEmailModel): Optional sender information
        notes (string): Optional notes (not displayed to customer)
        etid (string): The email template identifier

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "account_identifier":'accountIdentifier',
        "amount":'amount',
        "customer_identifier":'customerIdentifier',
        "send_email":'sendEmail',
        "utid":'utid',
        "campaign":'campaign',
        "email_subject":'emailSubject',
        "external_ref_id":'externalRefID',
        "message":'message',
        "recipient":'recipient',
        "sender":'sender',
        "notes":'notes',
        "etid":'etid'
    }

    def __init__(self,
                 account_identifier=None,
                 amount=None,
                 customer_identifier=None,
                 send_email=None,
                 utid=None,
                 campaign=None,
                 email_subject=None,
                 external_ref_id=None,
                 message=None,
                 recipient=None,
                 sender=None,
                 notes=None,
                 etid=None):
        """Constructor for the CreateOrderRequestModel class"""

        # Initialize members of the class
        self.account_identifier = account_identifier
        self.amount = amount
        self.customer_identifier = customer_identifier
        self.send_email = send_email
        self.utid = utid
        self.campaign = campaign
        self.email_subject = email_subject
        self.external_ref_id = external_ref_id
        self.message = message
        self.recipient = recipient
        self.sender = sender
        self.notes = notes
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
        account_identifier = dictionary.get('accountIdentifier')
        amount = dictionary.get('amount')
        customer_identifier = dictionary.get('customerIdentifier')
        send_email = dictionary.get('sendEmail')
        utid = dictionary.get('utid')
        campaign = dictionary.get('campaign')
        email_subject = dictionary.get('emailSubject')
        external_ref_id = dictionary.get('externalRefID')
        message = dictionary.get('message')
        recipient = raas.models.name_email_model.NameEmailModel.from_dictionary(dictionary.get('recipient')) if dictionary.get('recipient') else None
        sender = raas.models.name_email_model.NameEmailModel.from_dictionary(dictionary.get('sender')) if dictionary.get('sender') else None
        notes = dictionary.get('notes')
        etid = dictionary.get('etid')

        # Return an object of this model
        return cls(account_identifier,
                   amount,
                   customer_identifier,
                   send_email,
                   utid,
                   campaign,
                   email_subject,
                   external_ref_id,
                   message,
                   recipient,
                   sender,
                   notes,
                   etid)


