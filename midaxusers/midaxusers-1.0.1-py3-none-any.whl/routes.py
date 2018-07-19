from midaxusers.models import db, User, UserAttributes, verify_domain_rights, verify_unique_user_in_domain, verify_unique_email
from flask import Flask, jsonify, make_response, abort, request, current_app, Blueprint
from werkzeug.security import generate_password_hash, check_password_hash
from flask_httpauth import HTTPBasicAuth
from sqlalchemy import types, and_, or_

auth = HTTPBasicAuth()
api = Blueprint('api', __name__, url_prefix='/api/v1.0')

@api.route('/', methods=['GET'])
@api.route('/index', methods=['GET'])
@api.route('/user/attributes', methods=['GET'])
@auth.login_required
def index():
    return get_attributes(uuid = request.loggeduser.uuid)

@api.route('/users/<string:username>/attributes', methods=['GET'])
@auth.login_required
def get_user_attributes(username):
    loggeduser = request.loggeduser
    targetuser = User(username)
    if not verify_domain_rights(loggeduser, targetuser = targetuser):
        abort(403)

    return get_attributes(usertosearch=username)

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
        return jsonify(user = user.serialize(), user_attributes=dict(e.serialize() for e in attributes))

    abort(404)

@api.route('/domain/users/inactive', methods=['GET'])
@auth.login_required
def get_current_domain_users_inactive():
    return get_domain_users_inactive(request.loggeduser.domain)

@api.route('/domains/<string:domain>/users/inactive', methods=['GET'])
@auth.login_required
def get_domain_users_inactive(domain):
    return get_domain_users_int(domain, active = False)

@api.route('/domain/users', methods=['GET'])
@auth.login_required
def get_current_domain_users():
    return get_domain_users(request.loggeduser.domain)

@api.route('/domains/<string:domain>/users', methods=['GET'])
@auth.login_required
def get_domain_users(domain):
    return get_domain_users_int(domain, active = True)


@api.route('/domains/<string:domain>/users', methods=['GET'])
@auth.login_required
def get_domain_users_int(domain, active = True):
    loggeduser = request.loggeduser  
    domain = domain.casefold()

    if not verify_domain_rights(loggeduser, targetdomain = domain):
        abort(403)

    domainlevels = domain.split('^')
    current_domain_depth = ''    
        
    current_domain_depth = domainlevels[0]    
        
    for domainlevel in domainlevels[1:]: 
        if domainlevel is not None and len(domainlevel) > 0:
            current_domain_depth += '^{}'.format(domainlevel)
        
    current_domain_depth += '%'      

    users = User.query.filter(User.domain.like(current_domain_depth)).filter_by(active = active)

    if users is not None:
        return jsonify([e.serialize() for e in users])

    abort(404)

   

@api.route('/users/', methods=['POST'])
@auth.login_required
def create_user():
    if not request.json or not 'username' in request.json:
        abort(400)

    loggeduser = request.loggeduser

    try:
        newuser = User(username = request.json['username'], domain = request.json['domain'])
    except:
        abort(400)

    if newuser.domain is None:
        abort(400)

    if not verify_domain_rights(loggeduser, targetuser = newuser):
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
        newuser.force_password_change = request.json['force_password_change']
    except:
        newuser.force_password_change = False
    
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
    if not verify_domain_rights(loggeduser, targetuser = targetuser):
        abort(403)

    try:
        force_change = request.json['force_password_change']
    except:
        force_change = False

    try:
        password = request.json['password']
    except:
        abort(400)

    return change_password(newpassword = password, username = username, force_change = force_change)


@api.route('/user/password', methods=['POST'])
def reset_password():
    if not verify_pw_internal(request.authorization.username, request.authorization.password):
        return jsonify({'error': 'Unauthorized access'}), 401    

    try:
        password = request.json['password']
    except:
        abort(400)

    return change_password(newpassword = password, force_change = False)

def change_password(newpassword, uuid = None, username = None, force_change = False):

    if len(newpassword) < 0:
        abort(400)

    if uuid is not None:
        usertosearch = User(uuid = uuid)        
    elif username is not None:
        usertosearch = User(username)            
    else:
        usertosearch = request.loggeduser  
    
    user = usertosearch.search()  

    if user is None:
        abort(404)
        
    try:
        user.password = newpassword
        user.force_password_change = force_change
    except:
        abort(400)

    try:       
        db.session.commit()
    except:
        return jsonify({'error': "Cannot update password"}), 409

    return jsonify({'status': "SUCCESS"}), 200

@api.route('/users/<string:username>/deactivate', methods=['POST'])
@auth.login_required
def deactivate_user(username):
    loggeduser = request.loggeduser
    targetuser = User(username)
    if not verify_domain_rights(loggeduser, targetuser = targetuser):
        abort(403)
        
    founduser = targetuser.search()

    if founduser is None:
        abort(404)

    #UserAttributes.query.filter_by(user_uuid = founduser.uuid).delete()

    founduser.active = False

    try:       
        db.session.commit()
    except:
        return jsonify({'error': "Cannot deactivate user"}), 409

    return jsonify({'status': "SUCCESS"}), 200





#need to be the last routes
@api.route("/<path:missing>", methods=['PUT', 'PATCH', 'DELETE'])
@auth.login_required
def method_not_allowed_on_unknown_path(missing):
    abort(405)

@api.route("/<path:missing>")
@auth.login_required
def path_did_not_match(missing):
    abort(404)

@auth.verify_password
def verify_pw(username, password):
    if verify_pw_internal(username, password):
        if request.loggeduser.force_password_change == True:
            abort(423)
        return True
    return False

def verify_pw_internal(username, password):
    if username is None or password is None:
        return False
    usertosearch = User(username)    
    user = usertosearch.search()
    if user is not None:       
        request.loggeduser = user
        return user.check_password(password)
    return False


@api.errorhandler(405)
def not_allowed(error):
    return make_response(jsonify({'error': 'Method not allowed'}), 405)

@api.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@api.errorhandler(403)
def forbidden(error):
    return make_response(jsonify({'error': 'Access forbidden for user'}), 403)

@api.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)

@api.errorhandler(423)
def locked(error):
    return make_response(jsonify({'error': 'User has been locked, change password.'}), 423)

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)

