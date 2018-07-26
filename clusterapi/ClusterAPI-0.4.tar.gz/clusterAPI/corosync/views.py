from flask import Blueprint, make_response
from flask.views import MethodView
from clusterAPI.auth.helper import token_required
#test
corosync = Blueprint('corosync', __name__)


class CorosyncConf(MethodView):
    @token_required
    def get(self):
        return 'get corosync.conf'

    def post(self):
        return 'post corosync.conf'


conf_view = CorosyncConf.as_view('corosync')
corosync.add_url_rule('/corosync/conf', view_func=conf_view)
