from flask import json, request, Blueprint, jsonify
from evodoc.exception import DbException, ApiException
from evodoc.entity import *
from evodoc.api import response_ok, response_ok_list, response_ok_obj, validate_token

module = Blueprint('module', __name__, url_prefix='/module')

@module.route('/<int:id>', methods=['GET'])
def get_module_by_id_action(id):
    """
    Get module data by it's id
        :param id:
    """
    data = request.get_json()
    if data == None or data == {}:
        raise ApiException(404, "No data suplied")
    if ('token' not in data) or (data['token'] == None):
        raise ApiException(403, "Invalid token")
    token = data['token']
    validate_token(token)
    #check permissions in the future
    data = Module.get_module_by_id(Module, id)
    return response_ok_obj(data)

@module.route('/name/<name>', methods=['GET'])
def get_module_by_name_action(name):
    """
    Get module data by it's name
        :param name: Module name
    """
    token = request.args.get('token')
    validate_token(token)
    #check permissions in the future
    data = Module.get_module_by_name(Module, name)
    return response_ok_obj(data)

@module.route('/all', methods=['GET'])
def get_module_all_action():
    """
    Get data for all modules
    """
    data = request.get_json()
    if data == None or data == {}:
        raise ApiException(404, "No data suplied")
    if ('token' not in data) or (data['token'] == None):
        raise ApiException(403, "Invalid token")
    token = data['token']
    validate_token(token)
    #check permissions in the future
    resp = Module.get_module_all()
    return response_ok_list(resp)

@module.route('/project_id/<int:id>', methods=['GET'])
def get_module_all_by_project_id_action(id):
    """
    Get data for all modules in project
        :param id: Project ID
    """
    data = request.get_json()
    if data == None or data == {}:
        raise ApiException(404, "No data suplied")
    if ('token' not in data) or (data['token'] == None):
        raise ApiException(403, "Invalid token")
    token = data['token']
    validate_token(token)
    #check permissions in the future
    data = Module.get_module_all_by_project_id(Module, id)
    return response_ok_obj(data)

@module.route("/update_or_create", methods=['POST'])
def update_or_create_module_action():
    """
    Update or create module
    """
    data = request.get_json()
    if data == None:
        raise ApiException(400, "data")
    if (data['token'] == None):
        raise ApiException(403, "Invalid token")
    if (('module_id' not in data) or (data['module_id'] == None)):
        moduleId = None
    else:
        moduleId = data['module_id']
    validate_token(data['token'])
    #check permissions in the future
    data = Module.create_or_update_module_by_id_from_array(moduleId, data['data'])
    if (data == None):
        raise ApiException(400, "Name already in use.")
    return response_ok_obj(data)

@module.route("/build", methods=['POST'])
def build_module_action():
    """
    Update or create module
    """
    data = request.get_json()
    if data == None:
        raise ApiException(400, "data")
    if (data['token'] == None):
        raise ApiException(403, "Invalid token")
    if (('module_id' not in data) or (data['module_id'] == None)):
        raise ApiException(403, "Invalid module_id")
    else:
        moduleId = data['module_id']
    validate_token(data['token'])
    #check permissions in the future
    
    data = Module.get_module_by_id(moduleId).build_module()

    return response_ok(data)

@module.errorhandler(ApiException)
@module.errorhandler(DbException)
def __response_err(data):
    return jsonify(data.message), data.errorCode
