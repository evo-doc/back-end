from flask import json, request
from evodoc.exception import DbException, ApiException
from evodoc.app import app, db
from evodoc.entity import *
from evodoc.api import response_ok, response_err, response_ok_list, response_ok_obj, validate_token


@app.route('/project/<int:id>', methods=['GET'])
def get_project_by_id_action(id):
    """
    Get project data by it's id
        :param id:
    """
    try:
        token = request.args.get('token')
        validate_token(token)
        #check permissions in the future
        data = Project.get_project_by_id(Project, id)
        return response_ok_obj(data)
    except DbException as err:
        return response_err(err)
    except ApiException as err:
        return response_err(err)

@app.route('/project/name/<name>', methods=['GET'])
def get_project_by_name_action(name):
    """
    Get project data by it's name
        :param name: Project name
    """
    try:
        token = request.args.get('token')
        validate_token(token)
        #check permissions in the future
        data = Project.get_project_by_name(Project, name)
        return response_ok_obj(data)
    except DbException as err:
        return response_err(err)
    except ApiException as err:
        return response_err(err)

@app.route('/project/all', methods=['GET'])
def get_project_all_action():
    """
    Get data for all projects
    """
    try:
        token = request.args.get('token')
        validate_token(token)
        #check permissions in the future
        data = Project.get_project_all(Project)
        return response_ok_obj(data)
    except DbException as err:
        return response_err(err)
    except ApiException as err:
        return response_err(err)
