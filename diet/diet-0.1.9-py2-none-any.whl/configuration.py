import json
from os.path import expanduser, join

class DietConfiguration(object):

    def __init__(self, auth_client_id, auth_client_secret,
                 api_client_id, api_client_secret,
                 auth_verify_ssl, auth_host,
                 api_verify_ssl, api_host):
        self.auth_client_id = auth_client_id
        self.auth_client_secret = auth_client_secret
        self.api_client_id = api_client_id
        self.api_client_secret = api_client_secret
        self.auth_verify_ssl = auth_verify_ssl
        self.auth_host = auth_host
        self.api_verify_ssl = api_verify_ssl
        self.api_host = api_host

    @staticmethod
    def load_from_home_dir():
        home = expanduser('~')
        with open(join(home, '.diet', 'config.json')) as config_file:
            config = json.load(config_file)
            auth_client_id = config["auth"]["client_id"]
            auth_client_secret = config["auth"]["client_secret"]
            auth_host = config["auth"]["host"]
            auth_verify_ssl = config["auth"]["verify_ssl"]
            api_client_id = config["api"]["client_id"]
            api_client_secret = config["api"]["client_secret"]
            api_host = config["api"]["host"]
            api_verify_ssl = config["api"]["verify_ssl"]

            return DietConfiguration(auth_client_id=auth_client_id,
                auth_client_secret=auth_client_secret, api_client_id=api_client_id,
                api_client_secret=api_client_secret, auth_verify_ssl=auth_verify_ssl,
                auth_host=auth_host, api_host=api_host, api_verify_ssl=api_verify_ssl)