#needs to load connection from default file
from evodoc.app import *
#needs import UserToken
#import os

#from flask import Flask
#from flask_sqlalchemy import SQLAlchemy
#from flask_migrate import Migrate

#from sqlalchemy.engine import create_engine
#from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
import uuid
from flask_sqlalchemy_session import flask_scoped_session
from datetime import 	datetime, timedelta

#db = create_engine('postgresql://postgres:postgres@localhost:5432/postgres')



#Session = sessionmaker(bind=db)
#session = Session()
#Base = declarative_base()

def createToken (userId) : #creates new token and adds it to the database
	session = db.create_scoped_session(options=None)
	t = str(userId).zfill(10) + str(uuid.uuid4())
	while (session.query(UserToken).filter_by(token=t).count() != 0) :
		t = str(userId).zfill(10) + str(uuid.uuid4())
	session.add(UserToken(user_id=userId,token=t))
	session.commit()
	session.close()
	return t

def authenticateUser (id, token=None): #returns active token
	if (token==None) :
		return createToken(id)
	session = db.create_scoped_session(options=None)
	#make sure the token is active
	for token in session.query(UserToken).filter(UserToken.user_id==id, UserToken.created +  timedelta(hours=24) > datetime.utcnow(), UserToken.update +  timedelta(hours=2) > datetime.utcnow()):
		token.update=datetime.utcnow()#if token is active update it
		t=token.token
		session.commit()
		session.close()
		
		return t
	#otherwise createToken(id)
	session.close()
	return createToken(id)


authenticateUser(0,0)
#token = createToken(123456789)
#print(token)
