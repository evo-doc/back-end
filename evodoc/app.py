import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, upgrade
from sqlalchemy.orm import sessionmaker
import bcrypt

def create_app(additional_config = {}):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object('evodoc.appsettings.AppSettings')
    app.config.from_pyfile(os.path.dirname(__file__) + '/../conf/appsettings.local.ini')

    for key, value in additional_config.items():
        app.config[key] = value

    from evodoc.entity import db
    db.init_app(app)

    from evodoc.api import miscapi, module, package, permission, user

    app.register_blueprint(miscapi)
    app.register_blueprint(module)
    app.register_blueprint(package)
    app.register_blueprint(permission)
    app.register_blueprint(user)

    with app.app_context():
        from evodoc.entity.package import git_path
        git_path = app.config.get('GIT_PATH')

    return app

if __name__ == '__main__':
    app = create_app()

    if not os.path.exists(os.path.dirname(__file__) + '/' + app.config['GIT_PATH']):
        os.makedirs(os.path.dirname(__file__) + '/' + app.config['GIT_PATH'])

    git_path = os.path.dirname(__file__) + '/' + app.config['GIT_PATH']

    from evodoc.entity import db

    migrate = Migrate(app, db)
    #perform upgrade
    with app.app_context():
        upgrade(os.path.dirname(__file__) + '/../migrations')


    from evodoc.entity.seed.userseed import initUserSeeds
    from evodoc.api import *

    initUserSeeds()
    app.run(port=5000)
