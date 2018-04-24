from flask import json, request
from evodoc.exception import DbException, ApiException
from evodoc.app import app, db
from evodoc.login import login, authenticate, authenticateUser
from evodoc.entity import *
from evodoc.api import response_ok, response_err, response_ok_list, response_ok_obj, validate_token

@app.route('/user/<int:id>', methods=['GET'])
def get_user_by_id_action(id):
    """
    Get user data by it's id
        :param id:
    """
    try:
        token = request.args.get('token')
        validate_token(token)
        data = User.get_user_by_id(User, id)
        return response_ok_obj(data)
    except DbException as err:
        return response_err(err)
    except ApiException as err:
        return response_err(err)

@app.route('/user/<int:id>', methods=['DELETE'])
def delete_user(id):
    """
    Deletes user by it's id (only deactivation) 
        :param id:
    """
    try:
        token = request.args.get('token')
        validate_token(token)
        user = User.get_user_by_id(User, id)
        User.deactivate_user_by_id(user, user.id)
        data = {
            "data": "done"
        }
        return response_ok(data)
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
    if data == None:
        return response_err(ApiException(400, "Invalid data format"))
    if (data['username'] == None):
        err = ApiException(400, "No username provided")
        return response_err(err)
    if (data['password'] == None):
        err = ApiException(400, "No password provided")
        return response_err(err)
    try:
        token=login(data['username'], data['password'])
        data = {
            "token": token
        }
        return response_ok(data)
    except DbException as err:
        return response_err(err)

@app.route('/registration', methods=['POST'])
def registration_action():
    """
    Registration
    """
    try:
        data = request.get_json()
        if data == None:
            raise ApiException(400, "Invalid data format")
        if data['username'] == None:
            raise ApiException(400, "No username provided")
        if (data['email'] == None):
            raise ApiException(400, "No email provided")
        if (data['password'] == None):
            raise ApiException(400, "No password provided")

        if User.check_unique(User, data['username'], data['email'], True):
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

@app.route("/user/<int:id>/activation", methods=['POST'])
def activation_action(id):
    """
    Acc activation
    """
    try:
        data = request.get_json()
        if data == None:
            raise ApiException(400, "Invalid data format")
        if (data['token'] == None):
            err = ApiException(403, "Invalid token")
            return response_err(err)
        user = User.get_user_by_id(User, id)
        user.activation = True
        db.session.commit()
        data = {
            "data": "activated"
        }
        return response_ok(data)
    except ApiException as err:
        return response_err(err)
    except DbException as err:
        return response_err(err)
