from flask import json
from evodoc.exception import DbException
from evodoc.app import app
from evodoc.entity import *
from evodoc.api import response_ok, response_err, response_ok_list

@app.route('/user/<int:id>', methods=['GET'])
def get_user_by_id(id):
    try:
        data = User.get_user_by_id(User, id)
        return response_ok(data)
    except DbException as err:
        return response_err(err)
        
@app.route('/user/all/', methods=['GET'])
def get_user_all():
    try:
        data = User.get_user_all(User)
        return response_ok_list(data)
    except DbException as err:
        return response_err(err)
