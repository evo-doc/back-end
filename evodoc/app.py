import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('evodoc.appsettings.AppSettings')
app.config.from_pyfile(os.path.dirname(__file__) + '/../conf/appsettings.local.ini')

db = SQLAlchemy(app)
from evodoc.entity.models import User, UserType

migrate = Migrate(app, db)
