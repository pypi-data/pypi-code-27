# Standard library imports
import json
# Related third party imports
import urllib
import requests
# local application/library specific imports
from .data import Data
from .exceptions import ConfigurationException, UnsupportedException, JSONDecodeError
from .utils import sign, make_onboarding_token, get_kid, make_header_claims, make_uuid_4122, make_request


class Client(object):
    """
    Client for OpenID Connect (OIDC) methods, an authentication layer on top of OAuth 2.0, an authorization framework.

    """

    def __init__(self, signing_key=None, signing_public=None, transport_key=None, transport_public=None, *args,
                 **kwargs):
        """

        :param kwargs:
            - bank:
            - signing_key:
            - transport_key
            - transport_public

            - issuer: The issuer from the Well Known endpoint.
            - registration_endpoint: Dynamic Client Registration URL.
            - authorization_endpoint: Authorization endpoint from the Well Known.
            - well_known_token: Token URL from Well Known.
            - well_known_account_request_endpoint: Account request URL.

        """

        # Configuration properties.
        self.signing_key = signing_key
        self.transport_key = transport_key
        self.signing_public = signing_public
        self.transport_public = transport_public

        # Well-known kwarg properties.
        self.well_known_issuer = kwargs.get('issuer')
        self.well_known_registration = kwargs.get('registration_endpoint')
        self.well_known_authorization = kwargs.get('authorization_endpoint')
        self.well_known_token = kwargs.get('token_endpoint')

    @property
    def kid(self):
        """Returns the kid, parameter. (X.509 Certificate SHA-1 Thumbprint) of the signing certificate."""
        signing_public = self.signing_public
        if not signing_public:
            raise ConfigurationException("Signing was not  ")

        return get_kid(signing_public)

    def client_registration(self, ssa: str) -> Data:
        """v1.0.0 OpenBanking OpenID Connect Dynamic Client Registration.

        If supported by the ASPSP, this method allows TPP to submit an Software Statement Assertion (SSA)
        to an ASPSP in exchange for client credentials.

         +---------+                                      +----------------+                     +-----------+
         |         |                                      | Dynamic Client |                     |    OB     |
         | Client  |>--(1)- Register Client (with SSA) -->| Registration   |>--(1a) Validate --->| Directory |
         |  TPP    |<--(2)---- Client Credential --------<|    (ASPSP)     |<--(1b)--            |           |
         |         |                                      |                |                     |           |
         +---------+                                      +----------------+                     +-----------+

        Args:
            ssa: Software Statement Assertion (SSA). issued by OpenBanking identifier [RFC7519].

        Returns:
            class:`~openbanking.data.Data` Object that contains both response and status code of request.
                   ~openbanking.data.Data client_id : client identifier issued to the TPP.

        Raises:

        """
        header, claims = make_onboarding_token(
            kid=self.kid,
            aud=self.well_known_issuer,
            ssa=ssa,
        )

        payload = sign(header, claims, self.signing_key)
        headers = {'Content-Type': 'application/jwt'}
        cert = (self.transport_public, self.transport_key)
        response, status_code = make_request('post', self.well_known_registration,
                                             payload=payload,
                                             headers=headers,
                                             cert=cert,
                                             verify="/Users/glyn/Documents/workspace/openbanking/openbanking/certificates/ob/sandbox/ca.pem")
        return Data(response=response, status_code=status_code)

    def client_deregistration(self, ssa: str) -> Data:
        """v1.0.0 OpenBanking OpenID Connect Dynamic Client Deregistration.

        If supported by the ASPSP, same method as `client_registration` but allows a TPP to deregister an SSA to an ASPSP.

         +---------+                                        +----------------+
         |         |                                        | Dynamic Client |
         | Client  |>--(1)- Deregister Client (with SSA) -->| Registration   |
         |  TPP    |<--(2)---- HTTP Status 200   --------<  |    (ASPSP)     |
         |         |                                        |                |
         +---------+                                        +----------------+

       Args:
            ssa: Software Statement Assertion (SSA). issued by OpenBanking identifier [RFC7519].

        Returns:
            class:`~openbanking.data.Data` Object that contains both response and status code of request.

        Raises:


        """

        header, claims = make_onboarding_token(
            kid=self.kid,
            aud=self.well_known_issuer,
            ssa=ssa,
        )

        payload = sign(header, claims, self.signing_key)
        headers = {'Content-Type': 'application/jwt'}
        cert = (self.transport_public, self.transport_key)

        response, status_code = make_request('delete', self.well_known_registration,
                                             payload=payload,
                                             headers=headers,
                                             cert=cert,
                                             verify="/Users/glyn/Documents/workspace/openbanking/openbanking/certificates/ob/sandbox/ca.pem")

        return Data(response=response, status_code=status_code)

    def grant_client_credentials(self, client_id: str, scope: str, grant_type="client_credentials"):
        """ Client Credentials Grant OAuth 2.0 Authorization Server

        Gets an access token to represent you as a TPP using the Client credential flow.
        Client credential flow https://tools.ietf.org/html/rfc6749#section-4.4

         +---------+                                  +---------------+
         |         |                                  |               |
         |         |>--(A)- Client Authentication --->|     ASPSP     |
         | Client  |                                  |  Authorization|
         |         |                                  |     Server    |
         |         |<--(B)---- Access Token ---------<|               |
         |         |                                  |               |
         +---------+                                  +---------------+

        Args:
            client_id: the client identifier issued to the TPP during the registration process.
            scope: the scope of the access request.
            grant_type: value MUST be set to "client_credentials".

        Returns:

            class:`~openbanking.data.Data` Object that contains both response and status code of request.

        Raises:

        """

        header, claims = make_header_claims(
            kid=self.kid,
            iss=client_id,
            sub=client_id,
            aud=self.well_known_token,
        )

        client_assertion = sign(header, claims, self.signing_key)

        # TODO: allow different grant_type i.e. refresh on same endpoint.
        payload = dict(
            client_assertion_type='urn:ietf:params:oauth:client-assertion-type:jwt-bearer',
            grant_type=grant_type,
            client_id=client_id,
            client_assertion=client_assertion,
            scope=scope
        )

        cert = (self.transport_public, self.transport_key)
        response, status_code = make_request('post', self.well_known_token,
                                             payload=payload,
                                             headers={},
                                             cert=cert,
                                             verify=False)

        return Data(response=response, status_code=status_code)

    def get_access_token(self, authorization_code=None, grant_type="authorization_code", iss=None, sub=None):
        """


        """
        header, claims = make_header_claims(
            iss=iss,
            sub=sub,
            kid=self.kid,
            aud=self.well_known_token,
        )

        client_assertion = sign(header, claims, self.signing_key)

        redirect_uri = "https://getopenbanking.com/oauth2/callback"

        payload = dict(
            grant_type=grant_type,
            code=authorization_code,
            client_assertion_type='urn:ietf:params:oauth:client-assertion-type:jwt-bearer',
            client_assertion=client_assertion,
            redirect_uri=redirect_uri,

        )

        url = self.well_known_token
        cert = (self.transport_public, self.transport_key)
        response, status_code = make_request('post', url, payload=payload, headers={}, cert=cert, verify=False)
        return Data(response=response, status_code=status_code)

    def make_hybrid_psu_url(self, account_id: str, client_id: str):
        # TODO: loads more work here!
        """ OpenID Connect Hybrid Flow.

        Allows a TPP to initiate the hybrid flow in order to get an access token that contains the user's approval.

        Args:
            account_id:
            client_id:

        Returns:

            class:`~openbanking.data.Data` Object that contains both response and status code of request.

        Raises:

        Notes:




        You must complete the following steps as the TPP:

        This is initiated at the end of Step 2 by the AISP after the AccountRequestId is generated by the ASPSP and returned to the AISP.

        """

        data = dict(

            dict(id_token=dict(
                acr=dict(
                    value="urn:openbanking:psd2:sca",
                    essential=True
                ),
                openbanking_intent_id=dict(
                    value=account_id,
                    essential=True
                )
            )

            ),
            userinfo=dict(
                openbanking_intent_id=dict(
                    value=account_id,
                    essential=True
                )
            )

        )
        # TODO: should be be hardcoded
        scope = "accounts openid payments"
        response_type = "code id_token"
        redirect_uri = "https://getopenbanking.com/oauth2/callback"

        header, claims = make_header_claims(
            aud=self.well_known_issuer,
            kid=self.kid,
            iss=client_id,
            client_id=client_id,
            more_claims=data,
            scope=scope,
            response_type=response_type,
            redirect_uri=redirect_uri,
            state="5a6b0d7832a9fb4f80f1170a",
            nonce="5a6b0d7832a9fb4f80f1170a",

        )

        signed_token_request = sign(header, claims, self.signing_key)

        params = urllib.parse.urlencode(
            ([('client_id', client_id),
              ('redirect_uri', redirect_uri),
              ('response_type', response_type),
              ('scope', scope),
              ('request', signed_token_request),
              ]))

        pre = requests.Request('GET', "{}".format(self.well_known_authorization), params=params).prepare()
        return pre.url

    #
    # def account_requests_delete(self, account_request_id: str, access_token: str, transport_key=None,
    #                             transport_public=None):
    #     """
    #     """
    #     Delete account-request.
    #
    #     Usage:
    #         The DELETE /account-requests call allows an TPP to delete a previously created account-request
    #         (whether it is currently authorised or not). The PSU may want to remove their consent via the
    #         AISP instead of revoking authorisation with the ASPSP.
    #
    #    :param account_request_id: use to uniquely identify the account-request resource.
    #    :param access_token: TPP access token issued by the ASPSP using a client credentials grant.
    #
    #    return: class:`~openbanking.response.Session`
    #
    #     """
    #
    #     if not transport_key:
    #         transport_key = self.transport_key
    #
    #     if not transport_public:
    #         transport_public = self.transport_public
    #
    #         # TODO: these are common account headers, move them to a shared method.
    #     headers = {
    #         'Authorization': "Bearer {}".format(access_token),
    #         "Content-Type": "application/json",
    #         "Accept": "application/json",
    #         "x-fapi-financial-id": self.financial_id,
    #         "x-fapi-interaction-id": make_uuid_4122(),
    #     }
    #
    #     url = "{}/{}".format(self.account_requests_endpoint, account_request_id)
    #     print(url)
    #     cert = (transport_public, transport_key)
    #     make_request('delete', url, payload={}, headers=headers, cert=cert, verify=False)
    #     return self
    #
