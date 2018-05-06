import uuid
from evodoc.exception import DbException, ApiException
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
from evodoc.entity import db, UserToken, User
from sqlalchemy import desc

def login(username, password_plain):
	"""
	Login user, return his token as entity
		:param username:
		:param password_plain:
	"""
	user = User.get_user_by_username_or_email(username, False)
	if user is None:
		raise ApiException(400, 'userpass')
	if (user.confirm_password(password_plain)):
		if user.activated == False:
			token = authenticate(None, True, user.id)
			raise ApiException(200, {"verified": "false", "token": token.token})
		return authenticate(None, True, user.id)
	else:
		raise ApiException(400, 'userpass')

def authenticate(token = None, create_token = False, user_id = 0):
	"""
	Authenticate token, if token is not submited, it can be created, also if token is outdate, new one is returned
		:param token:
		:param create_token=False:
		:param user_id=0:
	"""
	if (token == None or token == {}) and create_token == False:
		return None
	elif create_token == True:
		User.get_user_by_id(user_id)
		new_token = str(user_id).zfill(10) + str(uuid.uuid4())
		#Check if token is unique
		while (UserToken.query.filter_by(token=new_token).count() != 0) :
			new_token = str(user_id).zfill(10) + str(uuid.uuid4())

		new_token = UserToken(user_id=user_id,token=new_token)
		db.session.add(new_token)
		db.session.commit()

		return new_token

	userTokenEntity = UserToken.query.filter_by(token=token).first()
	if userTokenEntity == None or (userTokenEntity.created + timedelta(hours=24) < datetime.utcnow() \
        and userTokenEntity.update + timedelta(hours=2) < datetime.utcnow()):
		return None
	if userTokenEntity.user.active != 1 or userTokenEntity.user.activated != 1:
		return None
	return userTokenEntity

def check_token_exists(token):
	return UserToken.query.filter((UserToken.token == token)).first()
