from flask import json, request, Blueprint, jsonify
from evodoc import DbException, ApiException, login, authenticate, check_token_exists, validate_email, validate_password, validate_username
from evodoc.entity import User, UserToken, Module, Project, Package
from evodoc.api import response_ok, response_ok_list, response_ok_obj, validate_token, validate_data

miscapi = Blueprint('miscapi', __name__)

@miscapi.route('/')
def home():
    """
    Some kind of homepage
    """
    return response_ok({"data": "This is evodoc backend api."})

@miscapi.route('/login', methods=['POST'])
def login_action():
    """
    API login entry point
    """
    data = request.get_json()
    validate_data(data, {'username', 'password'})
    token=login(data['username'], data['password'])
    data = {
        "token": token.token,
        "verified": "true"
    }
    return response_ok(data)

@miscapi.route('/registration', methods=['POST'])
def registration_action():
    """
    Registration
    """
    data = request.get_json()
    validate_data(data, {'username', 'password', 'email'})
    if not validate_email(data['email']):
        raise ApiException(400, "email")
    if not validate_username(data['username']):
        raise ApiException(400, "username")
    if not validate_password(data['password']):
        raise ApiException(400, "password")
    if User.check_unique(data['username'], data['email'], True):
        userEntity = User(data['username'], data['email'], data['password'])
        userEntity.save_entity()
        token = authenticate(None, True, userEntity.id)
        data = {
            "user_id": userEntity.id,
            "token": token.token
        }
        return response_ok(data)

@miscapi.route('/stats', methods=['GET'])
def stats():
    token = request.args.get('token')
    validate_token(token)
    user_count = User.query.count()
    module_count = Module.query.count()
    project_count = Project.query.count()
    package_count = Package.query.count()
    data = {
        'user_count': user_count,
        'module_count': module_count,
        'project_count': project_count,
        'package_count': package_count
    }
    return response_ok(data)

@miscapi.errorhandler(ApiException)
@miscapi.errorhandler(DbException)
def __response_err(data):
    return jsonify(data.message), data.errorCode

