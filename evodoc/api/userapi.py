from flask import json, request
from evodoc.exception import DbException, ApiException
from evodoc.app import app
from evodoc.login import login, authenticate
from evodoc.entity import *
from evodoc.api import response_ok, response_err, response_ok_list, response_ok_obj, validate_token

@app.route('/user/<int:id>', methods=['GET'])
def get_user_by_id(id):

    try:
        data = User.get_user_by_id(User, id)
        return response_ok_obj(data)
    except DbException as err:
        return response_err(err)

@app.route('/user/all/', methods=['GET'])
def get_user_all():
    """
    Get all user, only for logged users
    Token is taken from url param
    """
    try:
        token = request.args.get('token')
        userToken = validate_token(token)
        data = User.get_user_all(User)
        return response_ok_list(data)
    except DbException as err:
        return response_err(err)
    except ApiException as err:
        return response_err(err)


@app.route('/login', methods=['POST'])
def loginR():
    """
    API login entry point
    """
    data = request.get_json()
    if (data['username'] == None):
        err = DbException(400, "No username provided")
        return response_err(err)
    if (data['password'] == None):
        err = DbException(400, "No password provided")
        return response_err(err)
    try:
        token=login(data['username'], data['password'])
        return response_ok(token)
    except DbException as err:
        return response_err(err)
