# -*- coding: utf-8 -*-

"""
    raas.controllers.fund_controller

    This file was automatically generated for Tango Card, Inc. by APIMATIC v2.0 ( https://apimatic.io ).
"""

import logging
from .base_controller import BaseController
from ..api_helper import APIHelper
from ..configuration import Configuration
from ..http.auth.basic_auth import BasicAuth
from ..models.unregister_credit_card_response_model import UnregisterCreditCardResponseModel
from ..models.get_deposit_response_model import GetDepositResponseModel
from ..models.deposit_response_model import DepositResponseModel
from ..models.credit_card_model import CreditCardModel
from ..exceptions.raas_generic_exception import RaasGenericException

class FundController(BaseController):

    """A Controller to access Endpoints in the raas API."""

    def __init__(self, client=None, call_back=None):
        super(FundController, self).__init__(client, call_back)
        self.logger = logging.getLogger(__name__)

    def create_unregister_credit_card(self,
                                      body):
        """Does a POST request to /creditCardUnregisters.

        Unregister a credit card

        Args:
            body (UnregisterCreditCardRequestModel): TODO: type description
                here. Example: 

        Returns:
            UnregisterCreditCardResponseModel: Response from the API. 

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """
        try:
            self.logger.info('create_unregister_credit_card called.')
    
            # Validate required parameters
            self.logger.info('Validating required parameters for create_unregister_credit_card.')
            self.validate_parameters(body=body)
    
            # Prepare query URL
            self.logger.info('Preparing query URL for create_unregister_credit_card.')
            _query_builder = Configuration.get_base_uri()
            _query_builder += '/creditCardUnregisters'
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for create_unregister_credit_card.')
            _headers = {
                'accept': 'application/json',
                'content-type': 'application/json; charset=utf-8'
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for create_unregister_credit_card.')
            _request = self.http_client.post(_query_url, headers=_headers, parameters=APIHelper.json_serialize(body))
            BasicAuth.apply(_request)
            _context = self.execute_request(_request, name = 'create_unregister_credit_card')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for create_unregister_credit_card.')
            if _context.response.status_code == 0:
                raise RaasGenericException('API Error', _context)
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body, UnregisterCreditCardResponseModel.from_dictionary)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def get_deposit(self,
                    deposit_id):
        """Does a GET request to /creditCardDeposits/{depositId}.

        Get details for a specific credit card deposit

        Args:
            deposit_id (string): The reference deposit id

        Returns:
            GetDepositResponseModel: Response from the API. 

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """
        try:
            self.logger.info('get_deposit called.')
    
            # Validate required parameters
            self.logger.info('Validating required parameters for get_deposit.')
            self.validate_parameters(deposit_id=deposit_id)
    
            # Prepare query URL
            self.logger.info('Preparing query URL for get_deposit.')
            _query_builder = Configuration.get_base_uri()
            _query_builder += '/creditCardDeposits/{depositId}'
            _query_builder = APIHelper.append_url_with_template_parameters(_query_builder, { 
                'depositId': deposit_id
            })
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for get_deposit.')
            _headers = {
                'accept': 'application/json'
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for get_deposit.')
            _request = self.http_client.get(_query_url, headers=_headers)
            BasicAuth.apply(_request)
            _context = self.execute_request(_request, name = 'get_deposit')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for get_deposit.')
            if _context.response.status_code == 0:
                raise RaasGenericException('API Error', _context)
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body, GetDepositResponseModel.from_dictionary)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def add_funds(self,
                  body):
        """Does a POST request to /creditCardDeposits.

        Funds an account via credit card

        Args:
            body (DepositRequestModel): TODO: type description here. Example:
                
        Returns:
            DepositResponseModel: Response from the API. 

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """
        try:
            self.logger.info('add_funds called.')
    
            # Validate required parameters
            self.logger.info('Validating required parameters for add_funds.')
            self.validate_parameters(body=body)
    
            # Prepare query URL
            self.logger.info('Preparing query URL for add_funds.')
            _query_builder = Configuration.get_base_uri()
            _query_builder += '/creditCardDeposits'
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for add_funds.')
            _headers = {
                'accept': 'application/json',
                'content-type': 'application/json; charset=utf-8'
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for add_funds.')
            _request = self.http_client.post(_query_url, headers=_headers, parameters=APIHelper.json_serialize(body))
            BasicAuth.apply(_request)
            _context = self.execute_request(_request, name = 'add_funds')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for add_funds.')
            if _context.response.status_code == 0:
                raise RaasGenericException('API Error', _context)
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body, DepositResponseModel.from_dictionary)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def get_credit_cards(self):
        """Does a GET request to /creditCards.

        Retrieves all credit cards registered on the platform

        Returns:
            list of CreditCardModel: Response from the API. 

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """
        try:
            self.logger.info('get_credit_cards called.')
    
            # Prepare query URL
            self.logger.info('Preparing query URL for get_credit_cards.')
            _query_builder = Configuration.get_base_uri()
            _query_builder += '/creditCards'
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for get_credit_cards.')
            _headers = {
                'accept': 'application/json'
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for get_credit_cards.')
            _request = self.http_client.get(_query_url, headers=_headers)
            BasicAuth.apply(_request)
            _context = self.execute_request(_request, name = 'get_credit_cards')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for get_credit_cards.')
            if _context.response.status_code == 0:
                raise RaasGenericException('API Error', _context)
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body, CreditCardModel.from_dictionary)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def get_credit_card(self,
                        token):
        """Does a GET request to /creditCards/{token}.

        Retrieves details for a single credit card

        Args:
            token (string): Credit Card Token

        Returns:
            CreditCardModel: Response from the API. 

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """
        try:
            self.logger.info('get_credit_card called.')
    
            # Validate required parameters
            self.logger.info('Validating required parameters for get_credit_card.')
            self.validate_parameters(token=token)
    
            # Prepare query URL
            self.logger.info('Preparing query URL for get_credit_card.')
            _query_builder = Configuration.get_base_uri()
            _query_builder += '/creditCards/{token}'
            _query_builder = APIHelper.append_url_with_template_parameters(_query_builder, { 
                'token': token
            })
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for get_credit_card.')
            _headers = {
                'accept': 'application/json'
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for get_credit_card.')
            _request = self.http_client.get(_query_url, headers=_headers)
            BasicAuth.apply(_request)
            _context = self.execute_request(_request, name = 'get_credit_card')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for get_credit_card.')
            if _context.response.status_code == 0:
                raise RaasGenericException('API Error', _context)
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body, CreditCardModel.from_dictionary)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise

    def create_register_credit_card(self,
                                    body):
        """Does a POST request to /creditCards.

        Registers a new credit card

        Args:
            body (CreateCreditCardRequestModel): A CreateCreditCardRequest
                object

        Returns:
            CreditCardModel: Response from the API. 

        Raises:
            APIException: When an error occurs while fetching the data from
                the remote API. This exception includes the HTTP Response
                code, an error message, and the HTTP body that was received in
                the request.

        """
        try:
            self.logger.info('create_register_credit_card called.')
    
            # Validate required parameters
            self.logger.info('Validating required parameters for create_register_credit_card.')
            self.validate_parameters(body=body)
    
            # Prepare query URL
            self.logger.info('Preparing query URL for create_register_credit_card.')
            _query_builder = Configuration.get_base_uri()
            _query_builder += '/creditCards'
            _query_url = APIHelper.clean_url(_query_builder)
    
            # Prepare headers
            self.logger.info('Preparing headers for create_register_credit_card.')
            _headers = {
                'accept': 'application/json',
                'content-type': 'application/json; charset=utf-8'
            }
    
            # Prepare and execute request
            self.logger.info('Preparing and executing request for create_register_credit_card.')
            _request = self.http_client.post(_query_url, headers=_headers, parameters=APIHelper.json_serialize(body))
            BasicAuth.apply(_request)
            _context = self.execute_request(_request, name = 'create_register_credit_card')

            # Endpoint and global error handling using HTTP status codes.
            self.logger.info('Validating response for create_register_credit_card.')
            if _context.response.status_code == 0:
                raise RaasGenericException('API Error', _context)
            self.validate_response(_context)
    
            # Return appropriate type
            return APIHelper.json_deserialize(_context.response.raw_body, CreditCardModel.from_dictionary)

        except Exception as e:
            self.logger.error(e, exc_info = True)
            raise
