from flask import jsonify
from evodoc.exception import ApiException, DbException
from evodoc.login import authenticate, check_token_exists
from evodoc.entity import User, Module, Project, UserToken

def serialize_list(l):
    """
    Serialize data in list, for each class in list calls its serialize method at the end return whole list of serialized values
        :param l: List of objects which have serialize method
    """
    return [m.serialize() for m in l]

def response_ok_obj(data):
    """
    Returns object on which is serialized as json response
        :param data: object with serialize method
    """
    return jsonify(data.serialize())

def response_ok(data):
    """
    Converts data to json format and return them as server response
        :param data:
    """
    return jsonify(data)

def response_ok_list(data):
    """
    Converts list to list of serialized values and then send them as json response
        :param data: list of objects with serialize method
    """
    return jsonify(serialize_list(data))

def validate_token(token):
    """
    Validate token and return its instance
        :param token:
    """
    userToken = authenticate(token)
    if userToken == None:
        print(token)
        token = check_token_exists(token)
        if token is None:
            print(UserToken.query.filter_by(user_id = 1).first())
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
