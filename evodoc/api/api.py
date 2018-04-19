from flask import json
from evodoc.app import app

def response_ok(data):
    jsonData = json.dumps(data.serialize())
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
        status=data.code,
        minetype='application/json'
    )
    return response
