import time
import json
import requests
from werkzeug.contrib.cache import SimpleCache
# Application Libs
from .config import model_banks
from .exceptions import ConfigurationException, UnsupportedException, JSONDecodeError
from .utils import sign, make_onboarding_token, get_kid, make_header_claims, make_uuid_4122, make_request
from . import oidc
from .data import Data


class OpenBanking(oidc.Client):
    """
    A session stores configuration state.
    """

    def __init__(self, bank=None, transport_key=None, transport_public=None, access_token=None, *args, **kwargs):

        self.bank = bank

        self._response = None
        self._status_code = None

        # Inti load well-knows endpoints.
        well_known_url = self.get_config_args(bank, 'well_known')
        well_known_conf, status_code = make_request("get", well_known_url)
        if status_code is 200:
            kwargs.update(**well_known_conf)

        super().__init__(*args, **kwargs)

        # Configuration properties.
        self.transport_key = transport_key
        self.transport_public = transport_public
        self.access_token = access_token

    @property
    def response(self):
        return self._response

    @property
    def status_code(self):
        return self._status_code

    @property
    def resource_server(self):
        """Returns the account request endpoint"""
        url = self.get_config_args(self.bank, "resource_server")
        if not url:
            raise UnsupportedException()
        return url

    @property
    def financial_id(self):
        """Returns the financial id from the bank config if known."""

        bank = self.bank
        financial_id = self.get_config_args(bank, "financial_id")
        if not financial_id:
            raise UnsupportedException()
        return financial_id

    @staticmethod
    def _load_config_for_bank(bank_name: str) -> dict:
        """Returns a dictionary configuration for a particular Bank."""

        banks = [bank for bank in model_banks if bank['name'] == bank_name]
        if len(banks) != 1:
            raise ConfigurationException("Could not load bank configuration for {}.".format(bank_name))
        return banks[0]

    def get_config_args(self, bank: str, key: str) -> str:
        """Return a value from config."""
        bank_config = self._load_config_for_bank(bank)
        return bank_config.get(key, None)

    def account_transaction_requests(self, access_token: str, permissions: list) -> Data:
        """ v2.0 Open Banking Account and Transaction API Specification

        Send a copy of the consent to the ASPSP to authorise access to account and transaction information.

        Args:
            access_token: JWT access token issued by the ASPSP using a client credentials grant.
            permissions: specifies the Open Banking account request types.

        Returns:

            class:`~openbanking.data.Data` Object that contains both response and status code of request.

        Raises:

        Notes:
            AISPs must use a client credentials grant to obtain a token to access the account-requests resource.
            AISPs must use an authorization code grant to obtain a token to access all other resources.

        """

        # validation
        if not self.financial_id:
            raise ConfigurationException("Configuration error no financial ID")
        # TODO validate access_token
        # TODO look at permission scope validation.

        headers = {
            'Authorization': "Bearer {}".format(access_token),
            "Content-Type": "application/json",
            "Accept": "application/json",
            "x-fapi-financial-id": self.financial_id,
            "x-fapi-interaction-id": make_uuid_4122(),
        }

        payload = dict(
            Data=dict(
                Permissions=permissions
            ),
            Risk=dict()
        )
        payload = json.dumps(payload)
        cert = (self.transport_public, self.transport_key)

        print("{}{}".format(self.resource_server, "/account-request/"))

        response, status_code = make_request('post', "{}{}".format(self.resource_server, "/account-requests/"),
                                             payload=payload,
                                             headers=headers,
                                             cert=cert,
                                             verify=False)

        return Data(response=response, status_code=status_code)

    def accounts(self, account_id=None):
        """ v2.0 Accounts endpoint

        Supported:
            GET /accounts/{AccountId}
            GET /accounts

        Args:
            account_id: optional account id.

        Returns:

            class:`~openbanking.data.Data` Object that contains both response and status code of request.

        Raises:

        Notes:
            An TPP will be given the full list of accounts (the AccountId(s)) that the PSU has authorised
            The AccountId(s) returned may then be used to retrieve other resources for a specific AccountId.

        """

        headers = {
            'Authorization': "Bearer {}".format(self.access_token),
            "Content-Type": "application/json",
            "Accept": "application/json",
            "x-fapi-financial-id": self.financial_id,
            "x-fapi-interaction-id": make_uuid_4122(),
        }

        cert = (self.transport_public, self.transport_key)
        response, status_code = make_request('get', '{}/accounts'.format(self.resource_server),
                                             payload={},
                                             headers=headers,
                                             cert=cert,
                                             verify="/Users/glyn/Documents/workspace/openbanking/openbanking/certificates/ob/sandbox/ca.pem")

        return Data(response=response, status_code=status_code)
