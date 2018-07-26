from flask import Blueprint, make_response
from flask.views import MethodView
from app.common.helper import get_cib_data
from app.auth.helper import token_required

node = Blueprint('node', __name__)


class Cluster(MethodView):
    @token_required
    @get_cib_data("nodes")
    def get(self):
        return make_response(cib_data)

    def post(self):
        return 'post node'


# Cluster class as view
node_view = Cluster.as_view('node')
# Add rule for the api Endpoints
node.add_url_rule('/node', view_func=node_view)
