from dianping.auth import OAuth


class AuthorizePlatformRequest(OAuth):
    def __init__(self, app_key, app_secret):
        OAuth.__init__(self)
        self.set_app_key(app_key)
        self.set_secret(app_secret)
        self.set_grant_type('authorize_platform')
        self.set_httpmethod("POST")
        self.set_url('https://openapi.dianping.com/router/oauth/token')

    def set_grant_type(self, grant_type):
        self.add_query_param('grant_type', grant_type)

    def set_secret(self, secret):
        self.add_query_param('app_secret', secret)


class RefreshTokenRequest(OAuth):
    def __init__(self, app_key, app_secret, refresh_token):
        OAuth.__init__(self)
        self.set_app_key(app_key)
        self.set_secret(app_secret)
        self.set_grant_type('refresh_token')
        self.set_refresh_token(refresh_token)

        self.set_httpmethod("POST")
        self.set_url('https://openapi.dianping.com/router/oauth/token')

    def set_secret(self, secret):
        self.add_query_param('app_secret', secret)

    def set_grant_type(self, grant_type):
        self.add_query_param('grant_type', grant_type)

    def set_refresh_token(self, set_refresh_token):
        self.add_query_param('set_refresh_token', set_refresh_token)

'''
grant_type:
    authorization_code 
    refresh_token
    authorize_platform
'''
class DynamicTokenRequest(OAuth):
    def __init__(self, app_key, app_secret, auth_code, grant_type='authorization_code', redirect_url=None):
        OAuth.__init__(self)
        self.set_app_key(app_key)
        self.set_secret(app_secret)
        self.set_grant_type(grant_type)
        self.set_auth_code(auth_code)
        self.set_redirect_url(redirect_url)
        self.set_httpmethod("POST")
        self.set_url('https://openapi.dianping.com/router/oauth/token')

    def set_secret(self, secret):
        if secret is not None:
            self.add_query_param('app_secret', secret)

    def set_grant_type(self, grant_type):
        if grant_type is not None:
            self.add_query_param('grant_type', grant_type)

    def set_auth_code(self, auth_code):
        if auth_code is not None:
            self.add_query_param('auth_code', auth_code)

    def set_redirect_url(self, redirect_url):
        if redirect_url is not None:
            self.add_query_param(redirect_url)
