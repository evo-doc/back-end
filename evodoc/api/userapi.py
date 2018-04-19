from flask import json, request
from evodoc.exception import DbException
from evodoc.app import app
from evodoc.login import login
from evodoc.entity import *
from evodoc.api import response_ok, response_err, response_ok_list, response_ok_obj

@app.route('/user/<int:id>', methods=['GET'])
def get_user_by_id(id):
    try:
        data = User.get_user_by_id(User, id)
        return response_ok_obj(data)
    except DbException as err:
        return response_err(err)

@app.route('/user/all/', methods=['GET'])
def get_user_all():
    try:
        data = User.get_user_all(User)
        return response_ok_list(data)
    except DbException as err:
        return response_err(err)

@app.route('/login', methods=['POST'])
def loginR():
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
