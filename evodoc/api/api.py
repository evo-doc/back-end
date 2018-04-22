from flask import json
from evodoc.app import app

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
