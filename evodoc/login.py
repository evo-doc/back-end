import uuid
from evodoc.app import db
from evodoc.exception import DbException
from sqlalchemy.orm import sessionmaker
from flask_sqlalchemy_session import flask_scoped_session
from datetime import datetime, timedelta
from evodoc.entity import *

def login(username, password_plain):
	user = User.get_user_by_username_or_email(User, username)
	if user.activated == False:
		raise DbException(304, "User is not activated yet")
	if (user.confirm_password(password_plain)):
		return authenticateUser(user.id, None)

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
    t = UserToken.query.filter(UserToken.user_id==id, UserToken.created +  timedelta(hours=24) > datetime.utcnow(), UserToken.update + timedelta(hours=2) > datetime.utcnow()).order_by(desc(UserToken.created)).first()
    if (t == None):
        return createToken(id)
    t.update=datetime.utcnow()
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
	userTokenEntity = UserToken.query.filter((UserToken.token == token) or ((UserToken.created + timedelta(hours=24)) > datetime.now()) or ((UserToken.update +  timedelta(hours=2)) > datetime.now())).first()
	if userTokenEntity == None:
		return None
	if userTokenEntity.user.active != 1:
		return None
	return userTokenEntity

def check_token_exists(token):
	return userToken.query.filter((UserToken.token == token)).first()
