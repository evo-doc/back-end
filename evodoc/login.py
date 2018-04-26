import uuid
from evodoc.app import db
from evodoc.exception import DbException, ApiException
from sqlalchemy.orm import sessionmaker
from flask_sqlalchemy_session import flask_scoped_session
from datetime import datetime, timedelta
from evodoc.entity import *
from sqlalchemy import desc

def login(username, password_plain):
	user = User.get_user_by_username_or_email(User, username)
	if (user.confirm_password(password_plain)):
		if user.activated == False:
			token = authenticateUser(user.id)
			raise ApiException(200, {"verified": "false", "token": token})
		return authenticateUser(user.id, None)
	else:
		raise ApiException(403, "Invalid username or password.")

def createToken (userId) : #creates new token and adds it to the database
	t = str(userId).zfill(10) + str(uuid.uuid4())
	while (UserToken.query.filter_by(token=t).count() != 0) :
		t = str(userId).zfill(10) + str(uuid.uuid4())
	db.session.add(UserToken(user_id=userId,token=t))
	db.session.commit()
	return t

def authenticateUser (id, token=None): #returns active token
    if (token==None) :
        return createToken(id)
    t = UserToken.query.filter(UserToken.user_id==id, UserToken.created + timedelta(hours=24) > datetime.utcnow(), UserToken.update + timedelta(hours=2) > datetime.utcnow()).first()
    #.order_by(db.desc(UserToken.created))
    if (t == None):
        return createToken(id)
    t.update=datetime.datetime.utcnow()
    t.token = token
    db.session.commit()
    return t

def authenticate(token):
	"""
	Test if token exist, if not returns None, if its out of date, returns new token, else return old one
		:param token: user token
	"""
	if token == None:
		return None
	userTokenEntity = UserToken.query.filter_by(token=token).filter(UserToken.created > datetime.utcnow() + timedelta(hours=-24)).filter(UserToken.update > datetime.utcnow() + timedelta(hours=-2)).first() #.order_by(db.desc(UserToken.created))
	if userTokenEntity == None:
		return None
	if userTokenEntity.user.active != 1:
		return None
	return userTokenEntity

def check_token_exists(token):
	return UserToken.query.filter((UserToken.token == token)).first()
