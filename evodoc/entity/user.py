"""User: Contains all entities that are related to user
"""
import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from evodoc.app import db
import bcrypt
from evodoc.exception import DbException

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

    def get_user_by_id(self, userId):
        user = self.query.get(userId)
        if (user == None):
            raise DbException(DbException, 404, "No user found.")
        return user
        
    def get_user_all(self):
        user = self.query.all()
        if (user == None):
            raise DbException(DbException, 404, "No user found.")
        return user
        
    def update_user_type_by_id(self, id, userType):
        try:
            user = self.get_user_by_id(id)
        if (user == None):
            return False
        user.user_type_id = userType
        user.update = datetime.datetime.utcnow
        db.session.commit()
        return True
        
    def update_user_name_by_id(self, id, name):
        try:
            user = self.get_user_by_id(id)
        if (user == None):
            return False
        user.name = name
        user.update = datetime.datetime.utcnow
        db.session.commit()
        return True
        
    def update_user_email_by_id(self, id, email):
        try:
            user = self.get_user_by_id(id)
        if (user == None):
            return False
        user.email = email
        user.update = datetime.datetime.utcnow
        db.session.commit()
        return True
    
    def update_user_password_by_id(self, id, password):
        user = self.get_user_by_id(id)
        if (user == None):
            return False
        user.password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        user.update = datetime.datetime.utcnow
        db.session.commit()
        return True
        
    def update_user_name_by_id(self, id, name):
        try:
            user = self.get_user_by_id(id)
        if (user == None):
            return False
        user.name = name
        user.update = datetime.datetime.utcnow
        db.session.commit()
        return True
        
    def activate_user_by_id(self, id):
        try:
            user = self.get_user_by_id(id)
        if (user == None):
            return False
        user.active = True
        user.update = datetime.datetime.utcnow
        db.session.commit()
        return True
        
    def deactivate_user_by_id(self, id):
        try:
            user = self.get_user_by_id(id)
        if (user == None):
            return False
        user.active = False
        user.update = datetime.datetime.utcnow
        db.session.commit()
        return True
        

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'active': self.active,
        }

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

