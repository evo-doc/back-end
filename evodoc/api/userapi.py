from flask import json, request, Blueprint, jsonify
from evodoc.exception import DbException, ApiException
from evodoc.login import login, authenticate, check_token_exists
from evodoc.entity import User, UserToken, UserType
from evodoc.api import response_ok, response_ok_list, response_ok_obj, validate_token, validate_data
from datetime import datetime, timedelta

user = Blueprint('user', __name__, url_prefix='/user')

@user.route('', methods=['GET'])
def get_user_by_id_action():
    """
    Get user data by it's id
    """
    token = request.args.get('token')
    user_id = request.args.get('user_id')
    validate_token(token)
    data = User.get_user_by_id(user_id)
    return response_ok_obj(data)

@user.route('', methods=['DELETE'])
def delete_user():
    """
    Deletes user by it's id (only deactivation)
    """
    data = request.get_json()
    validate_data(data, {'token', 'user_id'})
    token = data['token']
    user_id = data['user_id']
    validate_token(token)
    user = User.get_user_by_id(user_id)
    User.deactivate_user_by_id(user.id)
    data = {
        "data": "done"
    }
    return response_ok(data)

@user.route('', methods=['POST'])
def update_user():
    """
    Update user with suplied data, now works only for email, password, name and user type
    """
    data = request.get_json()
    validate_data(data, {'token', 'user_id'})
    user_id = data['user_id']
    token = data['token']
    validate_token(token)
    user = User.update_user_by_id_from_array(user_id, data)
    return response_ok_obj(user)

@user.route('/all', methods=['GET'])
def get_user_all_action():
    """
    Get all user, only for logged users
    Token is taken from url param
    """
    token = request.args.get('token')
    validate_token(token)
    data = User.get_user_all()
    return response_ok_list(data)

@user.route("/activation", methods=['POST'])
def activation_action():
    """
    Acc activation
    """
    data = request.get_json()
    validate_data(data, {'token'})
    token = check_token_exists(data['token'])
    if token == None:
        raise ApiException(403, "Invalid token")
    if token.user.activated:
        raise ApiException(401, "User has been already activated.")
    #check code somehow
    token.user.update_activation_by_id(token.user.id, True)
    data = {
        "data": "activated"
    }
    return response_ok(data)

@user.route("/authorised", methods=['POST'])
def is_user_authorised():
    """
    Information about users token, whenever its valid token or not
    """
    data = request.get_json()
    validate_data(data, {'token', 'user_id'})
    token = check_token_exists(data['token'])
    if token == None\
        or (token.created + timedelta(hours=24) < datetime.utcnow() \
        and token.update + timedelta(hours=2) < datetime.utcnow())\
        or token.user.active == False:
        raise ApiException(403, "user is not authorised")
    user_id = data['user_id']
    if (user_id != token.user_id):
        raise ApiException(403, "Invalid token")
    tokenData = {
        "token": token.token
    }
    return response_ok(tokenData)

@user.errorhandler(ApiException)
@user.errorhandler(DbException)
def __response_err(data):
    return jsonify(data.message), data.errorCode
