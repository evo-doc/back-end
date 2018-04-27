from flask import json, request
from evodoc.exception import DbException, ApiException
from evodoc.app import app, db
from evodoc.entity import *
from evodoc.api import response_ok, response_err, response_ok_list, response_ok_obj, validate_token

@app.route('/module/<int:id>', methods=['GET'])
def get_module_by_id_action(id):
    """
    Get module data by it's id
        :param id:
    """
    try:
        data = request.get_json()
        if data == None or data == {}:
            return response_err(ApiException(404, "No data suplied"))
        if ('token' not in data) or (data['token'] == None):
            raise ApiException(403, "Invalid token")
        token = data['token']
        validate_token(token)
        #check permissions in the future
        data = Module.get_module_by_id(Module, id)
        return response_ok_obj(data)
    except DbException as err:
        return response_err(err)
    except ApiException as err:
        return response_err(err)

@app.route('/module/name/<name>', methods=['GET'])
def get_module_by_name_action(name):
    """
    Get module data by it's name
        :param name: Module name
    """
    try:
        token = request.args.get('token')
        validate_token(token)
        #check permissions in the future
        data = Module.get_module_by_name(Module, name)
        return response_ok_obj(data)
    except DbException as err:
        return response_err(err)
    except ApiException as err:
        return response_err(err)

@app.route('/module/all', methods=['GET'])
def get_module_all_action():
    """
    Get data for all modules
    """
    try:
        data = request.get_json()
        if data == None or data == {}:
            return response_err(ApiException(404, "No data suplied"))
        if ('token' not in data) or (data['token'] == None):
            raise ApiException(403, "Invalid token")
        token = data['token']
        validate_token(token)
        #check permissions in the future
        resp = Module.get_module_all()
        return response_ok_list(resp)
    except DbException as err:
        return response_err(err)
    except ApiException as err:
        return response_err(err)

@app.route('/module/project_id/<int:id>', methods=['GET'])
def get_module_all_by_project_id_action(id):
    """
    Get data for all modules in project
        :param id: Project ID
    """
    try:
        token = request.args.get('token')
        validate_token(token)
        #check permissions in the future
        data = Module.get_module_all_by_project_id(Module, id)
        return response_ok_obj(data)
    except DbException as err:
        return response_err(err)
    except ApiException as err:
        return response_err(err)

@app.route("/module/id/update", methods=['POST'])
def update_module_action():
    """
    Update or create module
    """
    try:
        data = request.get_json()
        if data == None:
            raise ApiException(400, "data")
        if (data['token'] == None):
            err = ApiException(403, "Invalid token")
            return response_err(err)
        if (('module_id' not in data) or (data['module_id'] == None)):
            moduleId = None
        else:
            moduleId = data['module_id']
        validate_token(data['token'])
        #check permissions in the future
        Module.create_or_update_module_by_id_from_array(moduleId, data['data'])
        data = {
            "data": "ok"
        }
        return response_ok(data)
    except ApiException as err:
        return response_err(err)
    except DbException as err:
        return response_err(err)
