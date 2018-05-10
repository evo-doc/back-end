from flask import json, request, Blueprint, jsonify
from evodoc.exception import DbException, ApiException
from evodoc.entity import *
from evodoc.api import response_ok, response_ok_list, response_ok_obj, validate_token

permission = Blueprint('permission', __name__, url_prefix='/permission')

@permission.route('/module/<int:id>', methods=['GET'])
def get_module_permission_by_id_action(id):
    """
    Get module permission by it's id
        :param id:
    """
    token = request.args.get('token')
    validate_token(token)
    #check permissions in the future
    data = ModulePerm.get_module_perm_by_id(ModulePerm, id)
    return response_ok_obj(data)

@permission.route('/module/user_id/<int:id>', methods=['GET'])
def get_module_permission_by_user_id_action(id):
    """
    Get all module permissions for by user id
        :param id:
    """
    token = request.args.get('token')
    validate_token(token)
    #check permissions in the future
    data = ModulePerm.get_module_perm_all_by_user_id(ModulePerm, id)
    return response_ok_obj(data)

@permission.route('/module/module_id/<int:id>', methods=['GET'])
def get_module_permission_by_modue_id_action(id):
    """
    Get all module permissions by module id
        :param id:
    """
    token = request.args.get('token')
    validate_token(token)
    #check permissions in the future
    data = ModulePerm.get_module_perm_all_by_module_id(ModulePerm, id)
    return response_ok_obj(data)

###############################################################################
@permission.route('/project/<int:id>', methods=['GET'])
def get_project_permission_by_id_action(id):
    """
    Get project permission by it's id
        :param id:
    """
    token = request.args.get('token')
    validate_token(token)
    #check permissions in the future
    data = ProjectPerm.get_project_perm_by_id(ProjectPerm, id)
    return response_ok_obj(data)

@permission.route('/project/user_id/<int:id>', methods=['GET'])
def get_project_permission_by_user_id_action(id):
    """
    Get project permission by it's users id
        :param id:
    """
    token = request.args.get('token')
    validate_token(token)
    #check permissions in the future
    data = ProjectPerm.get_project_perm_all_by_user_id(ProjectPerm, id)
    return response_ok_obj(data)

@permission.route('/project/project_id/<int:id>', methods=['GET'])
def get_project_permission_by_project_id_action(id):
    """
    Get project permission by it's projects id
        :param id:
    """
    token = request.args.get('token')
    validate_token(token)
    #check permissions in the future
    data = ProjectPerm.get_project_perm_all_by_project_id(ProjectPerm, id)
    return response_ok_obj(data)

@permission.errorhandler(ApiException)
@permission.errorhandler(DbException)
def __response_err(data):
    return jsonify(data.message), data.errorCode
