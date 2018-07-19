from dianping.auth import Sign

class POIMaintainQueryFlowStatusRequest(Sign):
    def __init__(self, app_key, app_secret, session, type, flowid):
        Sign.__init__(self)
        self.set_app_key(app_key)
        self.set_secret(app_secret)
        self.set_session(session)
        self.set_httpmethod('GET')
        self.set_url('https://openapi.dianping.com/router/poi/maintain/queryflowstatus')
        self.set_type(type)
        self.set_flowid(flowid)

    def set_type(self, type):
        self.add_query_param('type', type)

    def set_flowid(self, flowid):
        self.add_query_param('flowid', flowid)



