from flask import json, request, Blueprint
from evodoc.login import login, authenticate, check_token_exists
from evodoc.exception import DbException, ApiException
from evodoc.entity import User, UserToken, Module, Project, Package
from evodoc.api import response_ok, response_err, response_ok_list, response_ok_obj, validate_token, validate_data

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
    try:
        data = request.get_json()
        validate_data(data, {'username', 'password'})
        token=login(data['username'], data['password'])
        data = {
            "token": token.token,
            "verified": "true"
        }
        return response_ok(data)
    except ApiException as err:
        return response_err(err)
    except DbException as err:
        return response_err(err)

@miscapi.route('/registration', methods=['POST'])
def registration_action():
    """
    Registration
    """
    try:
        data = request.get_json()
        validate_data(data, {'username', 'password', 'email'})

        if User.check_unique(data['username'], data['email'], True):
            userEntity = User(data['username'], data['email'], data['password'])
            userEntity.save_entity()
            token = authenticate(None, True, userEntity.id)
            data = {
                "user_id": userEntity.id,
                "token": token.token
            }
            return response_ok(data)
    except ApiException as err:
        return response_err(err)
    except DbException as err:
        return response_err(err)

@miscapi.route('/stats', methods=['GET'])
def stats():
    try:
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
    except ApiException as err:
        return response_err(err)
    except DbException as err:
        return response_err(err)

