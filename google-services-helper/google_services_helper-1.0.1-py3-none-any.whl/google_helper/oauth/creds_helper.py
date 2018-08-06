# -*- coding: utf-8 -*-

import json

import google.oauth2.credentials
from google.oauth2 import service_account



def credentials_from_file(creds_file, scopes, auth_through_service_account=False):
    credentials = None;

    try:
        if auth_through_service_account:
            credentials = service_account.Credentials.from_service_account_info(json.load(open(creds_file, 'rb'), encoding='utf-8'), scopes=scopes)
        else:
            credentials = google.oauth2.credentials.Credentials(**json.load(open(creds_file, 'rb'), encoding='utf-8'))

    except IOError as err:
        raise IOError('error in loading credentials file from given path');

    return credentials


def credentials_from_string(creds_string, scopes, auth_through_service_account=False):
    credentials = None;

    if auth_through_service_account:
        credentials = service_account.Credentials.from_service_account_info(json.loads(creds_string, encoding='utf-8'),scopes=scopes)
    else:
        credentials = google.oauth2.credentials.Credentials(**json.loads(creds_string, encoding='utf-8'))

    return credentials


def credentials_from_dict(creds_dict, scopes, auth_through_service_account=False):
    credentials = None;

    if auth_through_service_account:
        credentials = service_account.Credentials.from_service_account_info(creds_dict, scopes=scopes)
    else:
        credentials = google.oauth2.credentials.Credentials(**creds_dict)
    return credentials


def credentials_to_dict(credentials):
    cdict = {'token': credentials.token,
                'refresh_token': credentials.refresh_token,
                'token_uri': credentials.token_uri,
                'client_id': credentials.client_id,
                'client_secret': credentials.client_secret,
                'scopes': credentials.scopes}
    return cdict




