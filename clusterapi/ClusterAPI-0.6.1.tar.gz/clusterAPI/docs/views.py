
from flask import Blueprint, jsonify
from flask.views import MethodView
from flask_swagger import swagger
from clusterAPI import api


docs = Blueprint('docs', __name__)


class Docs(MethodView):
    def get(self):
        return jsonify(swagger(api))


docs_view = Docs.as_view('docs')
docs.add_url_rule('/', view_func=docs_view)
