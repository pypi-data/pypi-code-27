
from flask import Blueprint, request
from flask.views import MethodView
from clusterAPI.auth.helper import check_pam, create_token
from clusterAPI.common.helper import response, response_auth

auth = Blueprint('auth', __name__)


class RegisterUser(MethodView):

    def post(self):
        """
        Register user to cluster
        ---
        parameters:
          - username: username
          - password: password
        responses:
          201:        
            description: token created
        """
        post_data = request.get_json() or request.form
        username = post_data.get('username')
        password = post_data.get('password')

        if username and password and check_pam(username, password):
            token = create_token(username)
            return response_auth('success', 'Successfully registered', token, 201)
        else:
            return response('failed', 'Must provide correct username and password', 400)


# Register classes as views
registration_view = RegisterUser.as_view('register')

# Add rules for the api Endpoints
auth.add_url_rule('/auth/register', view_func=registration_view)
