# -*- coding: utf-8 -*-

"""
    raas.models.get_orders_response_model

    This file was automatically generated for Tango Card, Inc. by APIMATIC v2.0 ( https://apimatic.io )
"""
import raas.models.page_model
import raas.models.order_summary_model

class GetOrdersResponseModel(object):

    """Implementation of the 'GetOrdersResponse' model.

    Represents the response from the get orders call

    Attributes:
        page (PageModel): Pagination information
        orders (list of OrderSummaryModel): An array of orders

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "page":'page',
        "orders":'orders'
    }

    def __init__(self,
                 page=None,
                 orders=None):
        """Constructor for the GetOrdersResponseModel class"""

        # Initialize members of the class
        self.page = page
        self.orders = orders


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
        page = raas.models.page_model.PageModel.from_dictionary(dictionary.get('page')) if dictionary.get('page') else None
        orders = None
        if dictionary.get('orders') != None:
            orders = list()
            for structure in dictionary.get('orders'):
                orders.append(raas.models.order_summary_model.OrderSummaryModel.from_dictionary(structure))

        # Return an object of this model
        return cls(page,
                   orders)


