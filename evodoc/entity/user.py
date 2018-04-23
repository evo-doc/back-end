"""User: Contains all entities that are related to user
"""
import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, desc
from evodoc.app import db
import bcrypt
from evodoc.exception import DbException

###################################################################################
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
        user = self.query.filter_by(id=userId).get(1)
        if (user == None):
            raise DbException(DbException, 404, "User not found.")
        return user
        
    def get_user_by_name(self, userName):
        user = self.query.filter_by(name=userName).get(1)
        if (user == None):
            raise DbException(DbException, 404, "User not found.")
        return user
        
    def get_user_by_email(self, userEmail):
        user = self.query.filter_by(email=userEmail).get(1)
        if (user == None):
            raise DbException(404, "User not found.")
        return user

    def get_user_by_username_or_email(self, username):
        user = self.query.filter((User.email == username) | (User.name == username)).first()
        if (user == None):
            raise DbException(404, "User not found.")
        return user

    def get_user_all(self):
        user = self.query.all()
        if (user == None):
            raise DbException(404, "No user found.")
        return user

    def get_user_all_by_user_type_id(self, userType):
        user = self.query.filter_by(user_type_id=userType).all()
        if (user == None):
            raise DbException(DbException, 404, "No user found.")
        return user

    def update_user_type_by_id(self, id, userType):
        user = self.get_user_by_id(id)
        if (user == None):
            return False
        user.user_type_id = userType
        user.update = datetime.datetime.utcnow
        db.session.commit()
        return True
        
    def update_user_name_by_id(self, id, name):
        user = self.get_user_by_id(id)
        if (user == None):
            return False
        user.name = name
        user.update = datetime.datetime.utcnow
        db.session.commit()
        return True
        
    def update_user_email_by_id(self, id, email):
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
        user = self.get_user_by_id(id)
        if (user == None):
            return False
        user.name = name
        user.update = datetime.datetime.utcnow
        db.session.commit()
        return True
        
    def activate_user_by_id(self, id):
        user = self.get_user_by_id(id)
        if (user == None):
            return False
        user.active = True
        user.update = datetime.datetime.utcnow
        db.session.commit()
        return True
        
    def deactivate_user_by_id(self, id):
        user = self.get_user_by_id(id)
        if (user == None):
            return False
        user.active = False
        user.update = datetime.datetime.utcnow
        db.session.commit()
        return True

    def confirm_password(self, password_plain):
        return True
        if (bcrypt.checkpw(password_plain.encode("utf-8"), self.password.encode("utf-8"))):
            return True
        else:
            return False

    def serialize(self):
        return {
            'id': self.id,
            'user_type_id': self.user_type_id,
            'name': self.name,
            'email': self.email,
            'created': self.created,
            'update': self.update,
            'active': self.active,
        }

###################################################################################
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
    
    def get_type_by_id(self, typeId):
        userType = self.query.filter_by(id=typeId).get(1)
        if (userType == None):
            raise DbException(DbException, 404, "UserType not found.")
        return userType
    
    def get_type_by_name(self, typeName):
        userType = self.query.filter_by(name=typeName).get(1)
        if (userType == None):
            raise DbException(404, "UserType not found.")
        return userType
    
    def get_type_all(self):
        userType = self.query.all()
        if (userType == None):
            raise DbException(404, "No userType found.")
        return userType
    
    def update_type_name_by_id(self, id, name):
        userType = self.get_type_by_id(id)
        if (userType == None):
            return False
        userType.name = name
        db.session.commit()
        return True
        
    def update_type_permisson_by_id(self, id, permission):
        userType = self.get_type_by_id(id)
        if (userType == None):
            return False
        userType.permission = permission
        db.session.commit()
        return True
    
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'permission_flag':self.permission_flag
        }

###################################################################################
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
    
    def get_token_by_id(self, tokenId):
        userToken = self.query.filter_by(id=tokenId).get(1)
        if (userToken == None):
            raise DbException(DbException, 404, "UserToken not found.")
        return token
    
    def get_token_by_user_id(self, userId):         #returns newest token for user
        userToken = self.query.filter_by(user_id=userId).order_by(desc(table1.mycol)).first()
        if (userToken == None):
            raise DbException(404, "UserToken not found.")
        return token
    
    def get_token_all(self):
        userToken = self.query.all()
        if (userToken == None):
            raise DbException(404, "No userToken found.")
        return token
    
    def get_token_all_by_user_id(self, userId):
        userToken = self.query.filter_by(user_id=userId).all()
        if (userToken == None):
            raise DbException(DbException, 404, "No userToken found.")
        return token
    
    def update_token_user_id_by_id(self, id, userId):
        userToken = self.get_token_by_id(id)
        if (userToken == None):
            return False
        userToken.userId = userId
        userToken.update = datetime.datetime.utcnow
        db.session.commit()
        return True
    
    def update_token_token_by_id(self, id, token):
        userToken = self.get_token_by_id(id)
        if (userToken == None):
            return False
        userToken.token = token
        userToken.update = datetime.datetime.utcnow
        db.session.commit()
        return True
    
    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'token': self.token,
            'created': self.create,
            'update': self.update
        }

