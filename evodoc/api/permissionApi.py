from flask import json, request
from evodoc.exception import DbException, ApiException
from evodoc.app import app, db
from evodoc.entity import *
from evodoc.api import response_ok, response_err, response_ok_list, response_ok_obj, validate_token

@app.route('/modulePermission/<int:id>', methods=['GET'])
def get_module_permission_by_id_action(id):
    """
    Get module permission by it's id
        :param id:
    """
    try:
        token = request.args.get('token')
        validate_token(token)
        data = ModulePerm.get_module_perm_by_id(ModulePerm, id)
        return response_ok_obj(data)
    except DbException as err:
        return response_err(err)
    except ApiException as err:
        return response_err(err)

@app.route('/modulePermission/user_id/<int:id>', methods=['GET'])
def get_module_permission_by_user_id_action(id):
    """
    Get module permission by it's users id
        :param id:
    """
    try:
        token = request.args.get('token')
        validate_token(token)
        data = ModulePerm.get_module_perm_by_user_id(ModulePerm, id)
        return response_ok_obj(data)
    except DbException as err:
        return response_err(err)
    except ApiException as err:
        return response_err(err)

@app.route('/modulePermission/module_id/<int:id>', methods=['GET'])
def get_module_permission_by_modue_id_action(id):
    """
    Get module permission by it's modules id
        :param id:
    """
    try:
        token = request.args.get('token')
        validate_token(token)
        data = ModulePerm.get_module_perm_by_module_id(ModulePerm, id)
        return response_ok_obj(data)
    except DbException as err:
        return response_err(err)
    except ApiException as err:
        return response_err(err)

###############################################################################
@app.route('/projectPermission/<int:id>', methods=['GET'])
def get_project_permission_by_id_action(id):
    """
    Get project permission by it's id
        :param id:
    """
    try:
        token = request.args.get('token')
        validate_token(token)
        data = ProjectPerm.get_project_perm_by_id(ProjectPerm, id)
        return response_ok_obj(data)
    except DbException as err:
        return response_err(err)
    except ApiException as err:
        return response_err(err)

@app.route('/projectPermission/user_id/<int:id>', methods=['GET'])
def get_project_permission_by_user_id_action(id):
    """
    Get project permission by it's users id
        :param id:
    """
    try:
        token = request.args.get('token')
        validate_token(token)
        data = ProjectPerm.get_project_perm_by_user_id(ProjectPerm, id)
        return response_ok_obj(data)
    except DbException as err:
        return response_err(err)
    except ApiException as err:
        return response_err(err)

@app.route('/projectPermission/project_id/<int:id>', methods=['GET'])
def get_project_permission_by_project_id_action(id):
    """
    Get project permission by it's projects id
        :param id:
    """
    try:
        token = request.args.get('token')
        validate_token(token)
        data = ProjectPerm.get_project_perm_by_project_id(ProjectPerm, id)
        return response_ok_obj(data)
    except DbException as err:
        return response_err(err)
    except ApiException as err:
        return response_err(err)
