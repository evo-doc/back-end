from flask import jsonify
from evodoc.exception import ApiException, DbException
from evodoc.login import authenticate, check_token_exists
from evodoc.entity import User, Module, Project

def serialize_list(l):
    return [m.serialize() for m in l]

def response_ok_obj(data):
    return jsonify(data.serialize())

def response_ok(data):
    return jsonify(data)

def response_ok_list(data):
    return jsonify(serialize_list(data))

def response_err(data):
    return jsonify(data.message), data.errorCode

def validate_token(token):
    """
    Validate token and return its instance
        :param token:
    """
    userToken = authenticate(token)
    if userToken == None:
        token = check_token_exists(token)
        if token is None:
            raise ApiException(403, "Invalid token.")
        if token.user.activated == False:
            raise ApiException(200, {"data": "User not activated", "token": authenticate(None, True, token.user_id).token})
        else:
            raise ApiException(403, "Invalid token.")
    return userToken.token

def validate_data(data, expected_values = []):
    """
    validate data by given array of keys
    """
    if data == None or data == {}:
        raise ApiException(400, "data")
    for value in expected_values:
        if value not in data or data[value] is None or data[value] == {}:
            raise ApiException(400, "data")
