from flask import json, request, Blueprint, jsonify
from evodoc.exception import DbException, ApiException
from evodoc.entity import *
from evodoc.api import response_ok, response_ok_list, response_ok_obj, validate_token

project = Blueprint('project', __name__, url_prefix='/project')

@project.route('',methods=['GET'])
def get_project_by_id_action():
    """
    Get project data by it's id
    """
    token = request.args.get('token')
    id = request.args.get('id')
    validate_token(token)
    #check permissions in the future
    data = Project.get_project_by_id(id)
    return response_ok_obj(data)

@project.route('/name', methods=['GET'])
def get_project_by_name_action(name):
    """
    Get project data by it's name
    """
    token = request.args.get('token')
    name = request.args.get('name')
    validate_token(token)
    #check permissions in the future
    data = Project.get_project_by_name(name)
    if (data == None):
        return response_err(ApiException(400, "Name already in use."))
    return response_ok_obj(data)

@project.route('/all', methods=['GET'])
def get_project_all_action():
    """
    Get data for all projects
    """
    token = request.args.get('token')
    validate_token(token)
    #check permissions in the future
    data = Project.get_project_all()
    return response_ok_list(data)

@project.route("/update_or_create", methods=['POST'])
def update_or_create_poject_action():
    """
    Update or create poject
    """
    data = request.get_json()
    if data == None:
        raise ApiException(400, "data")
    if (data['token'] == None):
        raise ApiException(403, "Invalid token")
    if (('poject_id' not in data) or (data['poject_id'] == None)):
        poject_id = None
    else:
        poject_id = data['poject_id']
    validate_token(data['token'])
    #check permissions in the future
    data = Project.create_or_update_project_by_id_array(poject_id, data['data'], True)
    if (data == None):
        raise ApiException(400, "Name already in use.")
    return response_ok_obj(data)

@project.errorhandler(ApiException)
@project.errorhandler(DbException)
def __response_err(data):
    return jsonify(data.message), data.errorCode
