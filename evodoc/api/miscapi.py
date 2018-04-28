from flask import json, request
from evodoc.app import app, db
from evodoc.login import login, authenticate, authenticateUser, createToken, check_token_exists
from evodoc.exception import DbException, ApiException
from evodoc.entity import User, UserToken, Module, Project
from evodoc.api import response_ok, response_err, response_ok_list, response_ok_obj, validate_token, validate_data

@app.route('/login', methods=['POST'])
def login_action():
    """
    API login entry point
    """
    data = request.get_json()
    if data == None  or data == {}:
        return response_err(ApiException(400, "data"))
    if ('username' not in data) or (data['username'] == None):
        err = ApiException(400, "username")
        return response_err(err)
    if ('password' not in data) or (data['password'] == None):
        err = ApiException(400, "password")
        return response_err(err)
    try:
        token=login(data['username'], data['password'])
        data = {
            "token": token,
            "verified": "true"
        }
        return response_ok(data)
    except ApiException as err:
        return response_err(err)
    except DbException as err:
        return response_err(err)

@app.route('/registration', methods=['POST'])
def registration_action():
    """
    Registration
    """
    try:
        data = request.get_json()
        if data is None or data == {}:
            raise ApiException(400, "data")
        if 'username' not in data or data['username'] == None:
            raise ApiException(400, "username")
        if 'email' not in data or (data['email'] == None):
            raise ApiException(400, "email")
        if 'password' not in data or (data['password'] == None):
            raise ApiException(400, "password   ")

        if User.check_unique(data['username'], data['email'], True):
            userEntity = User(data['username'], data['email'], data['password'])
            userEntity.save_entity()
            token = authenticateUser(userEntity.id)
            data = {
                "user_id": userEntity.id,
                "token": token
            }
            return response_ok(data)
    except ApiException as err:
        return response_err(err)
    except DbException as err:
        return response_err(err)

@app.route('/stats')
def stats():
    try:
        data = request.get_json()
        validate_data(data, {'token'})
        validate_token(data['token'])
        user_count = User.query.count()
        module_count = Module.query.count()
        project_count = Project.query.count()
        data = {
            'user_count': user_count,
            'module_count': module_count,
            'project_count': project_count
        }
        return response_ok(data)
    except ApiException as err:
        return response_err(err)
    except DbException as err:
        return response_err(err)

