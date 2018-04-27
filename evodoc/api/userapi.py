from flask import json, request
from evodoc.exception import DbException, ApiException
from evodoc.app import app, db
from evodoc.login import login, authenticate, authenticateUser, createToken, check_token_exists
from evodoc.entity import User, UserToken, UserType
from evodoc.api import response_ok, response_err, response_ok_list, response_ok_obj, validate_token
from datetime import datetime, timedelta

@app.route('/user', methods=['GET'])
def get_user_by_id_action():
    """
    Get user data by it's id
        :param id:
    """
    try:
        token = request.args.get('token')
        user_id = request.args.get('user_id')
        validate_token(token)
        data = User.get_user_by_id(user_id)
        return response_ok_obj(data)
    except DbException as err:
        return response_err(err)
    except ApiException as err:
        return response_err(err)

@app.route('/user', methods=['DELETE'])
def delete_user():
    """
    Deletes user by it's id (only deactivation)
        :param id:
    """
    try:
        data = request.get_json()
        if data == None or data == {}:
            return response_err(ApiException(404, "No data suplied"))
        if ('token' not in data) or (data['token'] == None):
            raise ApiException(403, "Invalid token")
        if ('user_id' not in data) or (data['user_id'] == None):
            raise ApiException(400, "user")
        token = data['token']
        user_id = data['user_id']
        validate_token(token)
        user = User.get_user_by_id(user_id)
        User.deactivate_user_by_id(user.id)
        data = {
            "data": "done"
        }
        return response_ok(data)
    except DbException as err:
        return response_err(err)
    except ApiException as err:
        return response_err(err)

@app.route('/user', methods=['POST'])
def update_user():
    """
    Update user with suplied data, now works only for email, password, name and user type
        :param id: integer user id
    """
    try:
        data = request.get_json()
        if data == None or data == {}:
            return response_err(ApiException(404, "No data suplied"))
        if ('token' not in data) or (data['token'] == None):
            raise ApiException(403, "Invalid token")
        if ('user_id' not in data) or (data['user_id'] == None):
            raise ApiException(400, "user")
        user_id = data['user_id']
        token = data["token"]
        validate_token(token)
        user = User.update_user_by_id_from_array(User, user_id, data)
        return response_ok_obj(user)
    except DbException as err:
        return response_err(err)
    except ApiException as err:
        return response_err(err)

@app.route('/user/all/', methods=['GET'])
def get_user_all_action():
    """
    Get all user, only for logged users
    Token is taken from url param
    """
    try:
        token = request.args.get('token')
        validate_token(token)
        data = User.get_user_all(User)
        return response_ok_list(data)
    except DbException as err:
        return response_err(err)
    except ApiException as err:
        return response_err(err)


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

@app.route("/user/activation", methods=['POST'])
def activation_action():
    """
    Acc activation
    """
    try:
        data = request.get_json()
        if data == None:
            raise ApiException(400, "data")
        if ('token' not in data) or (data['token'] == None):
            raise ApiException(403, "Invalid token")
        if ('user_id' not in data) or (data['user_id'] == None):
            raise ApiException(400, "user")
        user_id = data['user_id']
        user = User.get_user_by_id(user_id)
        token = check_token_exists(data['token'])
        if token == None:
            raise ApiException(403, "Invalid token")
        if user.activated:
            raise ApiException(401, "User has been already activated.")
        #check code somehow
        user.update_activation_by_id(user.id, True)
        data = {
            "data": "activated"
        }
        return response_ok(data)
    except ApiException as err:
        return response_err(err)
    except DbException as err:
        return response_err(err)

@app.route("/user-active", methods=['POST'])
def is_user_active():
    try:
        data = request.get_json()
        if data == None:
            raise ApiException(400, "data")
        if ('token' not in data) or (data['token'] == None):
            raise ApiException(403, "Invalid token")
        token = validate_token(data['token'])
        tokenData = {
            "token": token
        }
        return response_ok(tokenData)
    except ApiException as err:
        return response_err(err)
    except DbException as err:
        return response_err(err)

@app.route("/user/authorised", methods=['POST'])
def is_user_authorised():
    try:
        data = request.get_json()
        if data == None:
            raise ApiException(400, "data")
        if ('token' not in data) or (data['token'] == None):
            raise ApiException(403, "Invalid token")
        token = check_token_exists(data['token'])
        if token == None or token.created < datetime.utcnow() + timedelta(hours=-24) or token.update < datetime.utcnow() + timedelta(hours=-2) or token.user.active == False:
            raise ApiException(403, "user is not authorised")
        if ('user_id' not in data) or (data['user_id'] == None):
            raise ApiException(400, "user")
        user_id = data['user_id']
        if (user_id != token.user_id):
            raise ApiException(403, "Invalid token")
        tokenData = {
            "token": token.token
        }
        return response_ok(tokenData)
    except ApiException as err:
        return response_err(err)
    except DbException as err:
        return response_err(err)
