from flask import json
from evodoc.exception import DbException
from evodoc.app import app
from evodoc.entity import *
from evodoc.api import response_ok, response_err

@app.route('/user/<int:id>', methods=['GET'])
def get_user_by_id(id):
    try:
        data = User.user_by_id(User, id)
        return response_ok(data)
    except DbException as err:
        return response_err(err)
