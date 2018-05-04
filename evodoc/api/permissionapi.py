from flask import json, request, Blueprint
from evodoc.exception import DbException, ApiException
from evodoc.entity import *
from evodoc.api import response_ok, response_err, response_ok_list, response_ok_obj, validate_token

permission = Blueprint('permission', __name__, url_prefix='/permission')

@permission.route('/modulePermission/<int:id>', methods=['GET'])
def get_module_permission_by_id_action(id):
    """
    Get module permission by it's id
        :param id:
    """
    try:
        token = request.args.get('token')
        validate_token(token)
        #check permissions in the future
        data = ModulePerm.get_module_perm_by_id(ModulePerm, id)
        return response_ok_obj(data)
    except DbException as err:
        return response_err(err)
    except ApiException as err:
        return response_err(err)

@permission.route('/modulePermission/user_id/<int:id>', methods=['GET'])
def get_module_permission_by_user_id_action(id):
    """
    Get all module permissions for by user id
        :param id:
    """
    try:
        token = request.args.get('token')
        validate_token(token)
        #check permissions in the future
        data = ModulePerm.get_module_perm_all_by_user_id(ModulePerm, id)
        return response_ok_obj(data)
    except DbException as err:
        return response_err(err)
    except ApiException as err:
        return response_err(err)

@permission.route('/modulePermission/module_id/<int:id>', methods=['GET'])
def get_module_permission_by_modue_id_action(id):
    """
    Get all module permissions by module id
        :param id:
    """
    try:
        token = request.args.get('token')
        validate_token(token)
        #check permissions in the future
        data = ModulePerm.get_module_perm_all_by_module_id(ModulePerm, id)
        return response_ok_obj(data)
    except DbException as err:
        return response_err(err)
    except ApiException as err:
        return response_err(err)

###############################################################################
@permission.route('/projectPermission/<int:id>', methods=['GET'])
def get_project_permission_by_id_action(id):
    """
    Get project permission by it's id
        :param id:
    """
    try:
        token = request.args.get('token')
        validate_token(token)
        #check permissions in the future
        data = ProjectPerm.get_project_perm_by_id(ProjectPerm, id)
        return response_ok_obj(data)
    except DbException as err:
        return response_err(err)
    except ApiException as err:
        return response_err(err)

@permission.route('/projectPermission/user_id/<int:id>', methods=['GET'])
def get_project_permission_by_user_id_action(id):
    """
    Get project permission by it's users id
        :param id:
    """
    try:
        token = request.args.get('token')
        validate_token(token)
        #check permissions in the future
        data = ProjectPerm.get_project_perm_all_by_user_id(ProjectPerm, id)
        return response_ok_obj(data)
    except DbException as err:
        return response_err(err)
    except ApiException as err:
        return response_err(err)

@permission.route('/projectPermission/project_id/<int:id>', methods=['GET'])
def get_project_permission_by_project_id_action(id):
    """
    Get project permission by it's projects id
        :param id:
    """
    try:
        token = request.args.get('token')
        validate_token(token)
        #check permissions in the future
        data = ProjectPerm.get_project_perm_all_by_project_id(ProjectPerm, id)
        return response_ok_obj(data)
    except DbException as err:
        return response_err(err)
    except ApiException as err:
        return response_err(err)
