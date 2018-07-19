from midaxusers.models import db, User, UserAttributes, verify_domain_rights, verify_unique_user_in_domain, verify_unique_email
from flask import Flask, jsonify, make_response, abort, request, current_app, Blueprint
from werkzeug.security import generate_password_hash, check_password_hash
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()
api = Blueprint('api', __name__, url_prefix='/api/v1.0')

@api.route('/', methods=['GET'])
@api.route('/index', methods=['GET'])
@api.route('/user/attributes', methods=['GET'])
@auth.login_required
def index():
    return get_attributes()

@api.route('/users/<string:username>/attributes', methods=['GET'])
@auth.login_required
def get_user_attributes(username):
    loggeduser = request.loggeduser
    targetuser = User(username)
    if not verify_domain_rights(loggeduser, targetuser.domain):
        abort(403)

    return get_attributes(usertosearch=username)

@api.route('/users/', methods=['POST'])
@auth.login_required
def create_user():
    if not request.json or not 'username' in request.json:
        abort(400)

    loggeduser = request.loggeduser
    newuser = User(request.json['username'])
    if not verify_domain_rights(loggeduser, newuser.domain):
        abort(403)

    if not verify_unique_user_in_domain(newuser):
        return jsonify({'error': "Duplicate user in domain"}), 409
    
    newuser.email = request.json.get('email', "")
    if not verify_unique_email(newuser.email):
        return jsonify({'error': "User with this email exists"}), 409

    newuser.role = int(request.json['role'])
    if (newuser.role <= 0):
        abort(400)

    if len(request.json['password']) < 0:
        abort(400)

    try:
        newuser.password = request.json['password']
    except:
        abort(400)

    try:
        db.session.add(newuser)
        db.session.commit()
    except:
        return jsonify({'error': "Duplicate user"}), 409

    return jsonify({'user': newuser.serialize()}), 201


@api.route('/users/<string:username>/password', methods=['POST'])
@auth.login_required
def change_user_password(username):
    loggeduser = request.loggeduser
    targetuser = User(username)
    if not verify_domain_rights(loggeduser, targetuser.domain):
        abort(403)
        
    return change_password(newpassword = request.json['password'], usertosearch=username)

def get_attributes(uuid = None, usertosearch = None):
    if uuid is not None:
        usertosearch = User(uuid = uuid)
        user = usertosearch.search()
    elif usertosearch is not None:
        usertosearch = User(usertosearch)    
        user = usertosearch.search()
    else:
        usertosearch = User(auth.username())    
        user = usertosearch.search()

    if user is None:
        abort(404)
    
    attributes = UserAttributes.query.filter_by(user_uuid = user.uuid)
    if attributes is not None:
        return jsonify(user_uuid = user.uuid, user_attributes=dict(e.serialize() for e in attributes))

    abort(404)

def change_password(newpassword, uuid = None, usertosearch = None):

    if len(newpassword) < 0:
        abort(400)

    if uuid is not None:
        usertosearch = User(uuid = uuid)
        user = usertosearch.search()
    elif usertosearch is not None:
        usertosearch = User(usertosearch)    
        user = usertosearch.search()
    else:
        usertosearch = User(auth.username())    
        user = usertosearch.search()       

    if user is None:
        abort(404)
        
    try:
        user.password = newpassword
    except:
        abort(400)

    try:       
        db.session.commit()
    except:
        return jsonify({'error': "Cannot update password"}), 409

    return jsonify({'status': "SUCCESS"}), 200

#needs to be the last route
@api.route("/<path:missing>")
@auth.login_required
def error_handler(missing):
    abort(404)

@auth.verify_password
def verify_pw(username, password):
    if username is None or password is None:
        return False
    usertosearch = User(username)    
    user = usertosearch.search()
    if user is not None:
        request.loggeduser = user
        return user.check_password(password)
    return False


@api.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@api.errorhandler(403)
def forbidden(error):
    return make_response(jsonify({'error': 'Access forbidden for user'}), 403)

@api.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)

