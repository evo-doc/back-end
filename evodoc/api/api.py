from flask import json
from evodoc.app import app
from evodoc.exception import ApiException
from evodoc.login import authenticate, check_token_exists
from evodoc.entity import User, Module, Project

def serialize_list(l):
    return [m.serialize() for m in l]

def response_ok_obj(data):
    jsonData = json.dumps(data.serialize())
    response = app.response_class(
        response=jsonData,
        status=200,
        mimetype='application/json'
    )
    return response

def response_ok(data):
    jsonData = json.dumps(data)
    response = app.response_class(
        response=jsonData,
        status=200,
        mimetype='application/json'
    )
    return response

def response_ok_list(data):
    jsonData = json.dumps(serialize_list(data))
    response = app.response_class(
        response=jsonData,
        status=200,
        mimetype='application/json'
    )
    return response

def response_err(data):
    jsonData = json.dumps(data.message)
    response = app.response_class(
        response=jsonData,
        status=data.errorCode,
        mimetype='application/json'
    )
    return response

def validate_token(token):
    """
    Validate token and return its instance
        :param token:
    """
    if token == None:
       raise ApiException(403, "Invalid token.")

    userToken = authenticate(token)
    if userToken == None:
        if check_token_exists(token):
            raise ApiException(200, {"data": "User not activated", "token": token})
        raise ApiException(403, "Invalid token.")
    return userToken.token

def validate_data(data, expected_values):
    """
    validate data by given array of keys
    """
    if data == None or data == {}:
        raise ApiException(400, "data")
    for value in expected_values:
        if value not in data or data[value] is None or data[value] == {}:
            raise ApiException(400, value)
