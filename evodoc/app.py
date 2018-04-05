import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, upgrade

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('evodoc.appsettings.AppSettings')
app.config.from_pyfile(os.path.dirname(__file__) + '/../conf/appsettings.local.ini')

db = SQLAlchemy(app)
from evodoc.entity.models import User, UserType

migrate = Migrate(app, db)
#perform upgrade
with app.app_context():
    upgrade(os.path.dirname(__file__) + '/../migrations')


from evodoc.entity.seed.userseed import *

userInsert()
