from dash_auth import Configuration as AuthConfig, ApiClient as AuthClient
from dash_api import Configuration as ApiConfig, ApiClient as AppClient
from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import BackendApplicationClient

class ClientFactory(object):

    def __init__(self, configuration):
        self.configuration = configuration
        self.auth_access_token = None
        self.app_access_token = None

    def get_auth_api_client(self):
        if self.auth_access_token is None:
            self.auth_access_token = self.get_access_token(self.configuration.auth_client_id,
                                                    self.configuration.auth_client_secret)

        auth_config = AuthConfig()
        auth_config.access_token = self.auth_access_token
        auth_config.host = self.configuration.auth_host
        auth_config.verify_ssl = self.configuration.auth_verify_ssl
        auth_api_client = AuthClient(configuration=auth_config)
        return auth_api_client

    def get_app_api_client(self,):
        if self.app_access_token is None:
            self.app_access_token = self.get_access_token(self.configuration.api_client_id,
                                                    self.configuration.api_client_secret)
        api_config = ApiConfig()
        api_config.access_token = self.app_access_token
        api_config.host = self.configuration.api_host
        api_config.verify_ssl = self.configuration.api_verify_ssl
        app_api_client = AppClient(configuration=api_config)
        return app_api_client

    def get_access_token(self, client_id, client_secret):
        token_url = "{host}/connect/token".format(host=self.configuration.auth_host)
        client = BackendApplicationClient(client_id=client_id)
        oauth = OAuth2Session(client=client)
        token = oauth.fetch_token(token_url=token_url, client_id=client_id,
                                client_secret=client_secret,
                                verify=self.configuration.auth_verify_ssl)

        return token['access_token']