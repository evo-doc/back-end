#needs to load connection from default file
#needs import UserToken
import os

#from flask import Flask
#from flask_sqlalchemy import SQLAlchemy
#from flask_migrate import Migrate

from sqlalchemy.engine import create_engine
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
#login = Flask(__name__, instance_relative_config=True)
#login.config.from_object('evodoc.appsettings.AppSettings')
#login.config.from_pyfile(os.path.dirname(__file__) + '/../conf/appsettings.local.ini')
#from evodoc.entity.models import User, UserType, UserToken
import uuid

db = create_engine('postgresql://postgres:postgres@localhost:5432/postgres')

Session = sessionmaker(bind=db)
session = Session()
Base = declarative_base()

def createToken (userId) :
	token = str(userId).zfill(10) + str(uuid.uuid4())
	while session.query(UserToken).filter(UserToken.token=token).count() != 0 :
		token = str(userId).zfill(10) + str(uuid.uuid4())
	return token
	
def authenticateUser (id, token):
	for token in session.query(UserToken).filter(UserToken.userId=id).all():
		print(token.token)
		#check if it has active token
		#if so give it back
		#otherwise createToken(id)
	



token = createToken(123456789)
print(token)
