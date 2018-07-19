from dianping.auth import Sign


class OauthSessionQueryRequest(Sign):
    def __init__(self, app_key, app_secret, session):
        Sign.__init__(self)
        self.set_app_key(app_key)
        self.set_secret(app_secret)
        self.set_session(session)
        self.set_url('https://openapi.dianping.com/router/oauth/session/query')
        self.set_httpmethod('GET')


class CustomerKeyShopScopeRequest(Sign):
    def __init__(self, app_key, app_secret, session, bid):
        Sign.__init__(self)
        self.set_app_key(app_key)
        self.set_secret(app_secret)
        self.set_session(session)
        self.set_bid(bid)
        self.set_url("https://openapi.dianping.com/router/oauth/session/scope ")
        self.set_httpmethod('GET')

    def set_bid(self, bid):
        self.add_query_param('bid', bid)
