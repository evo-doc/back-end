from evodoc.app import app
from evodoc.entity import *

@app.route('/user/<int:id>', [METHOD=['GET']])
def get_user_by_id(id):
    return User.get_user_by_id(id).email