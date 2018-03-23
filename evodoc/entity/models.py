import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from evodoc.app import db

#todo: oddělit soubory podle užití napč User, Model, Package a dále v tomto souboru pouze importovat vše, neboť zde bude probíhat vlastní migrace a plnění daty

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

    def __init__(self, name=None, email=None, password=None, created=None, active=True):
        self.name = name
        self.email = email
        self.password = password
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
