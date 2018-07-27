
import pam
import jwt
import datetime

from flask import request, make_response, jsonify
from functools import wraps
from clusterAPI import api
from clusterAPI.common.helper import response


def create_token(username):
    exp = datetime.datetime.utcnow() + \
          datetime.timedelta(days=api.config.get('AUTH_TOKEN_EXPIRY_DAYS'),
                             seconds=api.config.get('AUTH_TOKEN_EXPIRY_SECONDS'))
    token_data = {
        'exp' : exp,
        'user': username
    }
    
    try:
        return jwt.encode(token_data, 
                          api.config['SECRET_KEY'],
                          algorithm='HS256')
    except Exception as e:
        return e


def decode_token(token):
    try:
        token_data = jwt.decode(token, api.config['SECRET_KEY'], algorithms='HS256')
        return token_data['user'], True
    except jwt.ExpiredSignatureError:
        return 'Signature expired, Please sign in again', False
    except jwt.InvalidTokenError:
        return 'Invalid token. Please sign in again', False


def check_pam(username, password):
    p = pam.pam()
    return p.authenticate(username, password)


def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None
  
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]
            except IndexError:
                return response('failed', 'Provide a valid auth token', 403)

        if not token:
            return response('failed', 'Token is missing', 401)
        token_res, status = decode_token(token)
        if not status:
            return response('failed', token_res, 401)
 
        return f(*args, **kwargs)
    return decorated_function
