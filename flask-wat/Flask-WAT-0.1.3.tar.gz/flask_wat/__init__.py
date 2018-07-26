from urllib.parse import urljoin

import requests


class Wat:

    def __init__(self, appid=None, is_qy=False, app=None):
        self.appid = appid
        self.is_qy = is_qy
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        base_url = app.config['WAT_BASE_URL']
        username = app.config['WAT_USERNAME']
        password = app.config['WAT_PASSWORD']
        verify = app.config.get('WAT_VERIFY')

        if not self.appid:
            self.appid = app.config['WX_APPID']

        path_prefix = '/qy' if self.is_qy else '/wx'
        self.url = urljoin(base_url, f'{path_prefix}/{self.appid}/token')

        self.wat_session = requests.Session()
        self.wat_session.auth = (username, password)
        self.wat_session.verify = verify

        self.session = requests.Session()

    def get_access_token(self):
        r = self.wat_session.get(self.url)
        return r.json()['access_token']

    def request(self, method, url, params={}, **kwargs):
        params['access_token'] = self.get_access_token()
        return self.session.request(method=method, url=url,
                                    params=params, **kwargs)

    def get(self, url, **kwargs):
        kwargs.setdefault('allow_redirects', True)
        return self.request('get', url, **kwargs)

    def post(self, url, data=None, json=None, **kwargs):
        return self.request('post', url, data=data, json=json, **kwargs)
