import requests
import json

from datetime import datetime as dt


class Client:
    bearer_token_refresh_interval = 3300 # 55 minutes, 3300 seconds
    bearer_token_retrieve_time = None
    bearer_token = None

    host = ''
    username = None
    password = None
    client_id = None
    client_secret = None
    entity_id = None
    headers = {}

    def __init__(self,
                 host,
                 username=None,
                 password=None,
                 client_id=None,
                 client_secret=None,
                 entity_id=None):
        self.host = host
        self.username = username
        self.password = password
        self.client_id = client_id
        self.client_secret = client_secret
        self.entity_id = entity_id
        self.bearer_token_retrieve_time = dt(1900, 1, 1)

        self.set_headers()

    def set_headers(self):
        self.headers = {}

        if self.client_id is None and self.client_secret is None:
            self.headers["apiAccessKeyId"] = self.username
            self.headers["apiSecretAccessKey"] = self.password
        elif self.username is None and self.password is None:
            if self.check_and_refresh_bearer_token():
                self.headers["Authorization"] = "Bearer %s" % (self.bearer_token)

        self.headers["Content-Type"] = "application/json"

        if self.entity_id is not None:
            self.headers["zuora-entity-ids"] = self.entity_id

    def check_and_refresh_bearer_token(self):
        time_diff = (dt.now() - self.bearer_token_retrieve_time).total_seconds

        if self.bearer_token is None or time_diff >= self.bearer_token_refresh_interval:
            payload = { "client_id": self.client_id, "client_secret": self.client_secret, "grant_type": "client_credentials" }
            url = "%s/%s" % (self.host, "oauth/token")
            res = requests.post(url, data=payload)

            if res.status_code == 200:
                res_json = json.loads(res.text)
                self.bearer_token_retrieve_time = dt.now()
                self.bearer_token = res_json["access_token"]
                return res.status_code == 200

    def get(self, endpoint, optional_headers=None):
        if optional_headers is not None:
            self.headers = self.merge_headers(optional_headers)

        url = "%s/%s" % (self.host, endpoint)

        return requests.get(url, headers=self.headers)

    def post(self, endpoint, payload=None, optional_headers=None):
        if optional_headers is not None:
            self.headers = self.merge_headers(optional_headers)

        url = "%s/%s" % (self.host, endpoint)
        data = json.dumps(payload)

        return requests.post(url=url, data=data, headers=self.headers)

    def put(self, endpoint, payload=None, optional_headers=None):
        if optional_headers is not None:
            self.headers = self.merge_headers(optional_headers)

        url = "%s/%s" % (self.host, endpoint)
        data = json.dumps(payload)

        return requests.put(url=url, data=data, headers=self.headers)

    def delete(self, endpoint, optional_headers=None):
        if optional_headers is not None:
            self.headers = self.merge_headers(optional_headers)

        url = "%s/%s" % (self.host, endpoint)

        return requests.delete(url=url, headers=self.headers)

    def merge_headers(self, h):
        headers = self.headers.copy()
        headers.update(h)

        return headers