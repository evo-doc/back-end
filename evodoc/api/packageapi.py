from flask import request
from evodoc import app, db, DbException, ApiException
from evodoc.entity import Package
from evodoc.api import response_ok, response_ok_obj, response_ok_list, response_err, validate_token, validate_data

@app.route('/package', methods=['GET'])
def get_package_by_id_action():
    """
    Get packge by id
    """
    try:
        token = request.args.get('token')
        validate_token(token)
        package_id = request.args.get('package_id')
        data = Package.get_package_by_id(package_id)
        return response_ok_obj(data)
    except DbException as err:
        return response_err(err)
    except ApiException as err:
        return response_err(err)

@app.route('/package/all', methods=['GET'])
def get_all_packages():
    """
    Return all packages
    """
    try:
        token = request.args.get('token')
        validate_token(token)
        return response_ok_list(Package.get_all_packages())
    except DbException as err:
        return response_err(err)
    except ApiException as err:
        return response_err(err)

@app.route('/package', methods=['POST'])
def save_package():
    try:
        data = request.get_json()
        validate_data(data, {'token'})
        validate_token(data['token'])
        package = Package.save_or_create(data)
        return response_ok_obj(package)
    except DbException as err:
        return response_err(err)
    except ApiException as err:
        return response_err(err)

@app.route('/package/down', methods=['POST'])
def download_package():
    try:
        data = request.get_json()
        validate_data(data, {'token', 'package_id'})
        package = Package.get_package_by_id(data['package_id'])
        package.download_package()
        return response_ok({'data': 'Done'})
    except DbException as err:
        return response_err(err)
    except ApiException as err:
        return response_err(err)

@app.route('/package', methods=['DELETE'])
def delete_package():
    """
    Deletes package
    """
    try:
        data = request.get_json()
        validate_data(data, {'token', 'package_id'})
        package = Package.get_package_by_id(data['package_id'])
        package.delete_package()
        data = {
            "data": "done"
        }
        return response_ok(data)
    except DbException as err:
        return response_err(err)
    except ApiException as err:
        return response_err(err)


