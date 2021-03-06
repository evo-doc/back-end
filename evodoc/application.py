import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, upgrade
from sqlalchemy.orm import sessionmaker
import bcrypt

def create_app(additional_config = {}):
    """
    Application factory, creating whole app context
        :param additional_config = {}: Additional config, altering configuration from file and local configuration
    """
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object('evodoc.appsettings.AppSettings')
    if os.path.isfile(os.path.dirname(__file__) + '/../conf/appsettings.local.ini'):
        app.config.from_pyfile(os.path.dirname(__file__) + '/../conf/appsettings.local.ini')

    if additional_config != {}:
        for key, value in additional_config.items():
            app.config[key] = value

    from evodoc.entity import db
    db.init_app(app)

    migrate = Migrate(app, db)
    #perform upgrade
    with app.app_context():
        upgrade(os.path.dirname(__file__) + '/../migrations')


    from evodoc.api import miscapi, module, project, package, permission, user

    app.register_blueprint(miscapi)
    app.register_blueprint(module)
    app.register_blueprint(project)
    app.register_blueprint(package)
    app.register_blueprint(permission)
    app.register_blueprint(user)

    from evodoc.seed.userseed import initUserSeeds

    with app.app_context():
        from evodoc.entity.package import git_path
        git_path = app.config.get('GIT_PATH')
        initUserSeeds()

    return app
