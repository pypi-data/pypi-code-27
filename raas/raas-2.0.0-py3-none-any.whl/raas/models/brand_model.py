# -*- coding: utf-8 -*-

"""
    raas.models.brand_model

    This file was automatically generated for Tango Card, Inc. by APIMATIC v2.0 ( https://apimatic.io )
"""
from raas.api_helper import APIHelper
import raas.models.item_model

class BrandModel(object):

    """Implementation of the 'Brand' model.

    Represents a Brand

    Attributes:
        brand_key (string): The brand key
        brand_name (string): The brand name
        disclaimer (string): The brand's disclaimer
        description (string): The brand's description
        short_description (string): The brand's short description
        terms (string): The brand's terms
        created_date (datetime): The date the brand was created
        last_update_date (datetime): The date the brand was last updated
        image_urls (dict<object, string>): A map of Image URLs
        status (string): The brand's status
        items (list of ItemModel): An array of Item objects

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "brand_key":'brandKey',
        "brand_name":'brandName',
        "disclaimer":'disclaimer',
        "description":'description',
        "short_description":'shortDescription',
        "terms":'terms',
        "created_date":'createdDate',
        "last_update_date":'lastUpdateDate',
        "image_urls":'imageUrls',
        "status":'status',
        "items":'items'
    }

    def __init__(self,
                 brand_key=None,
                 brand_name=None,
                 disclaimer=None,
                 description=None,
                 short_description=None,
                 terms=None,
                 created_date=None,
                 last_update_date=None,
                 image_urls=None,
                 status=None,
                 items=None):
        """Constructor for the BrandModel class"""

        # Initialize members of the class
        self.brand_key = brand_key
        self.brand_name = brand_name
        self.disclaimer = disclaimer
        self.description = description
        self.short_description = short_description
        self.terms = terms
        self.created_date = APIHelper.RFC3339DateTime(created_date) if created_date else None
        self.last_update_date = APIHelper.RFC3339DateTime(last_update_date) if last_update_date else None
        self.image_urls = image_urls
        self.status = status
        self.items = items


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
        brand_key = dictionary.get('brandKey')
        brand_name = dictionary.get('brandName')
        disclaimer = dictionary.get('disclaimer')
        description = dictionary.get('description')
        short_description = dictionary.get('shortDescription')
        terms = dictionary.get('terms')
        created_date = APIHelper.RFC3339DateTime.from_value(dictionary.get("createdDate")).datetime if dictionary.get("createdDate") else None
        last_update_date = APIHelper.RFC3339DateTime.from_value(dictionary.get("lastUpdateDate")).datetime if dictionary.get("lastUpdateDate") else None
        image_urls = dictionary.get('imageUrls')
        status = dictionary.get('status')
        items = None
        if dictionary.get('items') != None:
            items = list()
            for structure in dictionary.get('items'):
                items.append(raas.models.item_model.ItemModel.from_dictionary(structure))

        # Return an object of this model
        return cls(brand_key,
                   brand_name,
                   disclaimer,
                   description,
                   short_description,
                   terms,
                   created_date,
                   last_update_date,
                   image_urls,
                   status,
                   items)


