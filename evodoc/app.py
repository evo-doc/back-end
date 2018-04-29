import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, upgrade
from sqlalchemy.orm import sessionmaker
import bcrypt


app = Flask(__name__, instance_relative_config=True)
app.config.from_object('evodoc.appsettings.AppSettings')
app.config.from_pyfile(os.path.dirname(__file__) + '/../conf/appsettings.local.ini')

if not os.path.exists(os.path.dirname(__file__) + '/../packages_git/'):
    os.makedirs(os.path.dirname(__file__) + '/../packages_git/')

git_path = os.path.dirname(__file__) + '/../packages_git/'

db = SQLAlchemy(app)

from evodoc.entity import *

migrate = Migrate(app, db)
#perform upgrade
with app.app_context():
    upgrade(os.path.dirname(__file__) + '/../migrations')


from evodoc.entity.seed.userseed import *
from evodoc.api import *

initUserSeeds()


@app.route('/')
def home():
	return "hillo wrld"

#userInsert()
