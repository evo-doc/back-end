"""User: Contains all entities that are related to module and project
"""
import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from evodoc.app import db
import bcrypt

class Module(db.Model):
    __tablename__ = "module"
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer)
    name = Column(String(50), unique=True)
    created = Column(DateTime, default=datetime.datetime.utcnow)
    update = Column(DateTime, default=datetime.datetime.utcnow)
    active = Column(Boolean)
    data = Column(Json)

    def __init__(self, project_id=None, name=None, created=None, update=None, active=True, data=None):
    	self.project_id = project_id
    	self.name = name
    	self.created = created
    	self.update = update
    	self.active = active
    	self.data = data

    def __repr__(self):
        return "<Module %r>" % (self.name)

class Project(db.Model):
	__tablename__ = "project"
	id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    created = Column(DateTime, default=datetime.datetime.utcnow)
    update = Column(DateTime, default=datetime.datetime.utcnow)
    active = Column(Boolean)
	
	def __init__(self, name=None, created=None, update=None, active=True, data=None):
    	self.name = name
    	self.created = created
    	self.update = update
    	self.active = active
    	self.data = data

    def __repr__(self):
        return "<Project %r>" % (self.name)
