"""User: Contains all entities that are related to user
"""
import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from evodoc.app import db
import bcrypt

class User(db.Model):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    user_type_id =Column(Integer, ForeignKey("user_type.id"))
    name = Column(String(50), unique=True)
    email = Column(String(120), unique=True)
    password = Column(String(128))
    created = Column(DateTime, default=datetime.datetime.utcnow)
    update = Column(DateTime, default=datetime.datetime.utcnow)
    active = Column(Boolean)

    def __init__(self, name=None, email=None, password=None, created=None, update=None, active=True):
        self.name = name
        self.email = email
        self.password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        self.created = created
        self.active = active

    def __repr__(self):
        return "<User %r>" % (self.name)

class UserType(db.Model):
    __tablename__ = "user_type"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    permission_flag = Column(Integer)

    def __init__(self, name=None, permission_flag=0):
        self.name = name
        self.permission_flag = permission_flag

    def __repr__(self):
        return "<UserType %r>" % (self.name)


class UserToken(db.Model):
	__tablename__ = "user_token"
	id = Column(Integer, primary_key=True)
	user_id = Column(Integer)
	token = Column(String(47), unique=True)
	created = Column(DateTime, default=datetime.datetime.utcnow)
	update = Column(DateTime, default=datetime.datetime.utcnow)
	
	def __init__(self, user_id=None, token=None, created=None, update=None):
		self.user_id=user_id
		self.token=token
		self.created=created
		self.update=update
	
	def __repr__(self):
		return "<UserToken %r>" % (self.token)
