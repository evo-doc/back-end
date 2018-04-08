import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, upgrade
from sqlalchemy.orm import sessionmaker


app = Flask(__name__, instance_relative_config=True)
app.config.from_object('evodoc.appsettings.AppSettings')
app.config.from_pyfile(os.path.dirname(__file__) + '/../conf/appsettings.local.ini')

db = SQLAlchemy(app)
#engine = create_engine("postgres://")
#session_factory = sessionmaker(bind=db)

from evodoc.entity.models import User, UserType, UserToken

migrate = Migrate(app, db)
#perform upgrade
with app.app_context():
    upgrade(os.path.dirname(__file__) + '/../migrations')


from evodoc.entity.seed.userseed import *

from evodoc.login import *

@app.route('/')
def home():
	return "hillo wrld"

#userInsert()
