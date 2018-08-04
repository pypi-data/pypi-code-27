
import os, webbrowser
import random, threading, logging

import google_auth_oauthlib.flow

import flask #for temporary redirection server.
from flask import current_app, Blueprint

from . import creds_helper

#blueprint, which we register with temporary server app in Authorizer factory class.
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/authorize')
def authorize():
    print('\033[H\033[J')
    print ('now complete authorisation in your web browser.')
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(current_app.config['client_secret_path'], scopes=current_app.config['scopes'])
    flow.redirect_uri = flask.url_for('auth.oauth2callback', _external=True)
    authorization_url, state = flow.authorization_url(
        access_type=current_app.config['access_type'],
        include_granted_scopes=current_app.config['include_granted_scopes']
        )
    return flask.redirect(authorization_url)


@auth_bp.route('/oauth2callback')
def oauth2callback():
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(current_app.config['client_secret_path'], scopes=current_app.config['scopes'])
    flow.redirect_uri = flask.url_for('auth.oauth2callback', _external=True)
    
    authorization_response = flask.request.url
    flow.fetch_token(authorization_response=authorization_response)
    credentials = flow.credentials
    
    credentials_file = open(current_app.config['credentials_storage_path'], 'wb')
    credentials_json = flask.json.dump(creds_helper.credentials_to_dict(credentials), credentials_file)

    print('\033[H\033[J')
    print ('authorization completed successfully, credentials stored in {}'.format(current_app.config['credentials_storage_path']))
    shutdown_server()
    return 'credentials successfully stored in {}'.format(current_app.config['credentials_storage_path'])

def shutdown_server():
    func = flask.request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()




class Authorizer(object):

    def __init__(self, client_secret_path, credentials_storage_path, scopes, **kwargs):
        super(Authorizer, self).__init__()
        self.server_app = flask.Flask(__name__)
        self.server_app.secret_key = "somERandoMKey"

        self.server_app.config['client_secret_path'] = client_secret_path
        self.server_app.config['credentials_storage_path'] = credentials_storage_path
        self.server_app.config['scopes'] = scopes

        self.server_app.config['access_type'] = kwargs.get('access_type', 'offline')
        self.server_app.config['include_granted_scopes'] = kwargs.get('include_granted_scopes', 'true')

        self.server_app.register_blueprint(auth_bp)

    def authorize(self):
        log = logging.getLogger('werkzeug')
        log.setLevel(logging.ERROR)
        os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
        port = 5000 + random.randint(0, 999)
        url = 'http://127.0.0.1:{port}/authorize'.format(port=port)
        threading.Timer(1.25, lambda: webbrowser.open(url)).start()
        self.server_app.run(port=port, debug=False)



