import json
import os
import sys
import jwt
import requests

from calendar import timegm
from datetime import datetime
from jwt import DecodeError


def get_config_path():
    path = os.path.abspath(os.environ.get('VGS_CONFIG', 'config.yaml'))
    return path


def login(config, username, password):
    auth0_access_token = auth0_login(config, username, password)
    return keycloak_token_exchange(config, auth0_access_token)


def auth0_login(config, username, password):
    login_data = {
        "client_id": config.get("auth0_client_id"),
        "client_secret": config.get("auth0_client_secret"),
        "grant_type": "http://auth0.com/oauth/grant-type/password-realm",
        "username": username,
        "password": password,
        "scope": "openid",
        "realm": "Username-Password-Authentication"
    }
    login_headers = {
        "Content-Type": "application/json"
    }
    token_response = requests.post(config.get("auth0_url"), headers=login_headers, data=json.dumps(login_data))
    parsed_response = __parse_response(token_response)

    if "mfa_token" in parsed_response:
        print('Please enter your MFA code', file=sys.stderr)
        mfa = input('')
        mfa_token = parsed_response["mfa_token"]
        mfa_data = {
            "client_id": config.get("auth0_client_id"),
            "client_secret": config.get("auth0_client_secret"),
            "grant_type": "http://auth0.com/oauth/grant-type/mfa-otp",
            "username": username,
            "password": password,
            "scope": "openid",
            "realm": "Username-Password-Authentication",
            "otp": mfa,
            "mfa_token": mfa_token
        }
        mfa_headers = {
            "Content-Type": "application/json"
        }

        token_response = requests.post(config.get("auth0_url"), headers=mfa_headers, data=json.dumps(mfa_data))
    elif "error" in parsed_response:
        print("Unexpected error: {}, {}".format(parsed_response["error"],
                                                parsed_response.get("error_description", "")))
        sys.exit(1)

    return __parse_response(token_response)['access_token']


# https://github.com/keycloak/keycloak-documentation/blob/master/securing_apps/topics/token-exchange/token-exchange.adoc
def keycloak_token_exchange(config, auth0_access_token):
    token_exchange_url = config.get("kc_server_url") + '/realms/' + config.get(
        "kc_realm") + '/protocol/openid-connect/token'
    data = {
        'grant_type': 'urn:ietf:params:oauth:grant-type:token-exchange',
        'subject_token': auth0_access_token,
        'subject_issuer': config.get("kc_oidc_provider_alias"),
        'subject_token_type': 'urn:ietf:params:oauth:token-type:access_token',
        'audience': config.get("kc_client_id")
    }
    response = requests.post(token_exchange_url, data=data,
                             auth=(config.get("kc_client_id"), config.get("kc_client_secret")))
    return __parse_response(response)['access_token']


def valid_expiration(token):
    decoded_token = jwt.decode(token, verify=False)
    now = timegm(datetime.utcnow().utctimetuple())

    try:
        exp = int(decoded_token['exp'])
    except ValueError:
        raise DecodeError('Expiration Time claim (exp) must be an'
                          ' integer.')

    if exp < now:
        print('Credentials are expired. Please re-enter.', file=sys.stderr)
        return False

    return True


def __parse_response(response):
    try:
        return json.loads(response.text)
    except Exception as ex:
        raise ex
